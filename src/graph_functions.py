
import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial.distance import directed_hausdorff
from shapely.ops import nearest_points, split, linemerge, snap, substring
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString
import momepy
import osmnx as ox
import networkx as nx
import math



##############################

def get_angle(linestring1, linestring2):

    '''
    Function for getting the smallest angle between two lines.
    Does not consider the direction of lines: I.e. is the angle larger than 90, it is instead expressed as 180 - original angle.

    Parameters
    ----------
    linestring1: Shapely geometry

    linestring2: Shapely geometry

    Returns
    -------
    angle_deg: float
        angle expressed in degrees

    '''

    arr1 = np.array(linestring1.coords)
    arr1 = arr1[1] - arr1[0]

    arr2 = np.array(linestring2.coords)
    arr2 = arr2[1] - arr2[0]

    angle = np.math.atan2(np.linalg.det([arr1,arr2]),np.dot(arr1,arr2))
    angle_deg = abs(np.degrees(angle))

    if angle_deg > 90:
        angle_deg = 180 - angle_deg

    return angle_deg


##############################

def get_hausdorff_dist(osm_edge, ref_edge):

    '''
    Computes the Hausdorff distance (max distance) between two LineStrings.

    Parameters
    ----------

    osm_edge: Shapely LineString
        The first geometry to compute Hausdorff distance between.

    ref_edge: Shapely LineString
        Second geometry to be used in distance calculation.

    Returns
    -------
    hausdorff_dist: float
        The Hausdorff distance.

    '''

    osm_coords = list(osm_edge.coords)
    ref_coords = list(ref_edge.coords)

    hausdorff_dist = max(directed_hausdorff(osm_coords, ref_coords)[0], directed_hausdorff(ref_coords, osm_coords)[0])

    return hausdorff_dist

 

##############################

def find_matches_buffer(geom, spatial_index, osm_data):

    possible_matches_index = list(spatial_index.intersection(geom.bounds))
    possible_matches = osm_data.iloc[possible_matches_index]

    precise_matches = possible_matches[possible_matches.intersects(geom)]
    precise_matches_index = list(precise_matches.index)

    return precise_matches_index

##############################

def return_buffer_matches(reference_data, osm_data, ref_id_col, dist):

    assert osm_data.crs == reference_data.crs, 'Data not in the same crs!'

    reference_buff = reference_data[[ref_id_col, 'geometry']].copy(deep=True)
    reference_buff.geometry = reference_buff.geometry.buffer(distance=dist)

    # Create spatial index on osm data
    osm_sindex = osm_data.sindex

    reference_buff['matches_index'] = reference_buff['geometry'].apply(lambda x: find_matches_buffer(x, osm_sindex, osm_data))

    # Drop geometry column
    reference_buff.drop('geometry', axis=1, inplace=True)

    # Only return rows with a result
    reference_buff['count'] = reference_buff['matches_index'].apply(lambda x: len(x))
    reference_buff = reference_buff[reference_buff['count'] > 1]
  
    return reference_buff

##############################

def get_segments(linestring, seg_length):

    org_length = linestring.length

    no_segments = math.ceil(org_length / seg_length)

    start = 0
    end = seg_length
    lines = []

    for _ in range(no_segments):

        assert start != end

        l = substring(linestring, start, end)
      
        lines.append(l)

        start += seg_length
        end += seg_length
    
    # If the last segment is too short, merge it with the one before
    for i, l in enumerate(lines):
        if l.length < seg_length/3:
            new_l = linemerge((lines[i-1], l))

            lines[i-1] = new_l

            del lines[i]

    lines = MultiLineString(lines)
    
    return lines


##############################

def merge_multiline(line_geom):

    if line_geom.geom_type == 'MultiLineString':
        line_geom = linemerge(line_geom)

    return line_geom


##############################

def create_segment_gdf(gdf, segment_length):

    gdf['geometry'] = gdf['geometry'].apply(lambda x: merge_multiline(x))
    assert gdf.geometry.geom_type.unique()[0] == 'LineString'

    gdf['geometry'] = gdf['geometry'].apply(lambda x: get_segments(x, segment_length))
    segments_gdf = gdf.explode(index_parts=False, ignore_index=True)

    ids = []
    for i in range(1000, 1000+len(segments_gdf)):
        ids.append(i)

    segments_gdf['seg_id'] = ids
    assert len(segments_gdf['seg_id'].unique()) == len(segments_gdf)


    return segments_gdf

##############################

# Function for finding the best out of potential/possible matches
def find_best_match(buffer_matches, ref_index, osm_edges, reference_edge, angular_threshold, hausdorff_threshold):

    potential_matches = osm_edges[['osmid','geometry']].loc[buffer_matches.loc[ref_index,'matches_index']].copy(deep=True)

    potential_matches['hausdorff_dist'] = potential_matches['geometry'].apply(lambda x: get_hausdorff_dist(osm_edge=x, ref_edge=reference_edge))
    potential_matches['angle'] = potential_matches['geometry'].apply(lambda x: get_angle(x, reference_edge))

    # Find matches within thresholds out of all matches for this referehce geometry
    potential_matches_subset = potential_matches[ (potential_matches.angle < angular_threshold) & (potential_matches.hausdorff_dist < hausdorff_threshold)].copy()

    if len(potential_matches_subset) == 0:
        
        best_osm_ix = None

    elif len(potential_matches_subset) == 1:
        best_osm_ix = potential_matches_subset.index.values[0]

    else:

        # Get match(es) with smallest Hausdorff distance and angular tolerance
        potential_matches_subset['hausdorff_dist'] = pd.to_numeric(potential_matches_subset['hausdorff_dist'] )
        potential_matches_subset['angle'] = pd.to_numeric(potential_matches_subset['angle'])
        
        best_matches_index = potential_matches_subset[['hausdorff_dist','angle']].idxmin()
        best_matches = potential_matches_subset.loc[best_matches_index].copy(deep=True)
        
        best_matches = best_matches[~best_matches.index.duplicated(keep='first')] # Duplicates may appear if the same edge is the one with min dist and min angle

        if len(best_matches) == 1:

            best_osm_ix = best_matches.index.values[0]

        elif len(best_matches) > 1: # Take the one with the smallest hausdorff distance
            
            best_match_index = best_matches['hausdorff_dist'].idxmin()
            best_match = potential_matches_subset.loc[best_match_index].copy(deep=True)
            best_match = best_match[~best_match.index.duplicated(keep='first')]
    
            best_osm_ix = best_match.name 

    return best_osm_ix


##############################

def find_matches_from_buffer(buffer_matches, osm_edges, reference_data, angular_threshold=30, hausdorff_threshold=12):

    matched_data = reference_data.loc[buffer_matches.index].copy(deep=True)

    matched_data['matches_ix'] = matched_data.apply(lambda x: find_best_match(buffer_matches, ref_index=x.name, osm_edges=osm_edges, reference_edge=x['geometry'], angular_threshold=angular_threshold, hausdorff_threshold=hausdorff_threshold), axis=1)
    
    matched_data.dropna(inplace = True)

    matched_ids = osm_edges.loc[matched_data.matches_ix, 'osmid'].values
    matched_data['osmid'] = matched_ids


    print(f'{len(matched_data)} reference segments where matched to OSM edges')

    print(f'{ len(reference_data) - len(matched_data) } reference segments where not matched')
    
    return matched_data

##############################

def update_osm(osm_segments, ref_segments, osm_data, reference_data, final_matches, attr, org_ref_id_col):

    ids_attr_dict = summarize_matches(osm_segments, ref_segments, reference_data, final_matches, attr, org_ref_id_col)

    attr_df = pd.DataFrame.from_dict(ids_attr_dict, orient='index')
    attr_df.reset_index(inplace=True)
    attr_df.rename(columns={'index':'org_osmid',0:attr}, inplace=True)

    updated_osm = osm_data.merge(attr_df, left_on='osmid', right_on='org_osmid', how='left')

    return updated_osm

##############################

# TODO: Make more efficient!
def summarize_matches(osm_segments, ref_segments, reference_data, final_matches, attr, org_ref_id_col):

    # Create dataframe with new and old ids and information on matches
    osm_merged = osm_segments.merge(final_matches.drop('geometry',axis=1), how='left', on='osmid')
    ref_attr = ref_segments.merge(reference_data[[org_ref_id_col,attr]], on=org_ref_id_col)
    ref_attr.drop('geometry',axis=1, inplace=True)
    osm_merged = osm_merged.merge(ref_attr[['seg_id',attr]], on='seg_id', how='left')

    org_ids = list(osm_merged['org_osmid'].unique())

    matched_attributes = {}

    for i in org_ids:
        
        feature = osm_merged.loc[osm_merged.org_osmid == i].copy(deep=True)
        feature[attr] = feature[attr].fillna('none')

        matched_values = feature[attr].unique()
        if len(matched_values) == 1:
            matched_attributes[i] = matched_values[0]

        else:
            feature['length'] = feature.geometry.length
            summed = feature.groupby(attr).agg({'length': 'sum'})
            majority_value = summed['length'].idxmax()
            matched_attributes[i] = majority_value

    return matched_attributes   

##############################

def create_node_index(x, index_length, add_letter='R'):
    '''
    Function for creating unique index column of specific length based on another shorter column.
    Possibility of adding additional letter for identifying ID (useful when creating 'false' OSM IDs)
    '''

    x = str(x)
    x  = x.zfill(index_length)
    
    assert len(x) == index_length

    if add_letter:
        x = x + 'R'

    return x

##############################

def find_parallel_edges(edges):

    '''
    Check for parallel edges in a pandas DataFrame with edges, including columns u with start node index and v with end node index.
    If two edges have the same u-v pair, the column 'key' is updated to ensure that the u-v-key combination can uniquely identify an edge.
    '''

    # Find edges with duplicate node pairs
    parallel = edges[edges.duplicated(subset=['u','v'])]

    edges.loc[parallel.index, 'key'] = 1 #Set keys to 1

    k = 1

    while len(edges[edges.duplicated(subset=['u','v','key'])]) > 0:

        k += 1

        parallel = edges[edges.duplicated(subset=['u','v','key'])]

        edges.loc[parallel.index, 'key'] = k #Set keys to 1

    assert len(edges[edges.duplicated(subset=['u','v','key'])]) == 0, 'Edges not uniquely indexed by u,v,key!'

    return edges


##############################

def create_osmnx_graph(gdf):

    ''''
    Function for  converting a geodataframe with LineStrings to a NetworkX graph object (MultiDiGraph), which follows the data structure required by OSMnx.
    (I.e. Nodes indexed by osmid, nodes contain columns with x and y coordinates, edges is multiindexed by u, v, key).
    Converts MultiLineStrings to LineStrings - assumes that there are no gaps between the lines in the MultiLineString

    OBS! Current version does not fix topology.

    Parameters
    ----------
    gdf: GeoDataFrame
        The data to be converted to a graph format
    directed: bool
        Whether the resulting graph should be directed or not. Directionality is based on the order of the coordinates.

    Returns
    -------
    graph: NetworkX MultiDiGraph object
        The original data in a NetworkX graph format.

    '''

    gdf['geometry'] = gdf['geometry'].apply( lambda x: linemerge(x) if x.geom_type == 'MultiLineString' else x)

    # If Multilines cannot be merged do to gaps, use explode
    geom_types = gdf.geom_type.to_list()
    #unique_geom_types = set(geom_types)

    if 'MultiLineString' in geom_types:
        gdf = gdf.explode(index_parts=False)

    # TODO: Convert linestrings to edges?
    G = momepy.gdf_to_nx(gdf, approach='primal', directed=True)

    nodes, edges = momepy.nx_to_gdf(G)

    # Create columns and index as required by OSMnx
    index_length = len(str(nodes['nodeID'].iloc[-1].item()))
    nodes['osmid'] = nodes['nodeID'].apply(lambda x: create_node_index(x, index_length))

    # Create x y coordinate columns
    nodes['x'] = nodes.geometry.x
    nodes['y'] = nodes.geometry.y

    edges['u'] = nodes['osmid'].loc[edges.node_start].values
    edges['v'] = nodes['osmid'].loc[edges.node_end].values

    nodes.set_index('osmid', inplace=True)

    edges['length'] = edges.geometry.length # Length is required by some functions

    edges['key'] = 0

    edges = find_parallel_edges(edges)

    # Create multiindex in u v key format
    edges = edges.set_index(['u', 'v', 'key'])

    # For ox simplification to work, edge geometries must be dropped. Edge geometries is defined by their start and end node
    #edges.drop(['geometry'], axis=1, inplace=True) # Not required by new simplification function


    G_ox = ox.graph_from_gdfs(nodes, edges)

   
    return G_ox


##############################

def explode_multilinestrings(gdf):

    individual_linestrings = gdf.explode(index_parts=True)

    new_ix_col = ['_'.join(map(str, i)) for i in zip(individual_linestrings.index.get_level_values(0), individual_linestrings.index.get_level_values(1))]
    individual_linestrings['index_split'] =  new_ix_col
    individual_linestrings.set_index('index_split', inplace=True)

    return individual_linestrings

##############################

def clean_col_names(df):
    '''
    Remove upper-case letters and : from OSM key names
    '''
    df.columns = df.columns.str.lower()

    df_cols = df.columns.to_list()

    new_cols = [c.replace(':','_') for c in df_cols]

    df.columns = new_cols

    return df
    
#%%
if __name__ == '__main__':

    # TODO: Move test data to this directory
    # Test merge multiline function
    line1 = LineString([[1,0],[10,0]])
    line2 = LineString([[10,0],[12,0]])
    multiline = MultiLineString([line1, line2])
    geoms = [line1, line2, multiline]
    test_gdf = gpd.GeoDataFrame(geometry=geoms)

    test_gdf['geometry'] = test_gdf['geometry'].apply(lambda x: merge_multiline(x))

    assert test_gdf.geometry.geom_type.unique()[0] == 'LineString'

    # Test get_angle function
    linestring1 = LineString([[0,0],[10,10]])
    linestring2 = LineString([[0,0],[10,0]])
    linestring3 = LineString([[10,0],[0,0]])

    angle1 = get_angle(linestring1, linestring2)

    angle2 = get_angle(linestring2, linestring1)

    angle3 = get_angle(linestring1, linestring3)

    assert round(angle1, 5) == round(angle2, 5) == round(angle3, 5), 'Angle test failed!'

    # Test get_hausdorff_dist function
    line1 = LineString([[1,1],[10,10]])
    line2 = LineString([[2,1],[4,3]])
    line3 = LineString([[4,3],[2,1]])

    h1 = get_hausdorff_dist(line1, line2)
    h2 = get_hausdorff_dist(line2, line1)
    h3 = get_hausdorff_dist(line1, line3)

    h4 = LineString([[1,1],[10,1]])
    h5 = LineString([[10,1],[20,1]])
    h4 = get_hausdorff_dist(h4, h5)

    assert h1 == h2 == h3, 'Hausdorff distance test failed!'
    assert h4 == 10, 'Hausdorff distance test failed!'

    test_data = gpd.read_file('../tests/geodk_test.gpkg')

    # Test create osmnx graph function
    test_graph = create_osmnx_graph(test_data)

    assert test_graph.is_directed() == True, 'Failed test for create osmnx graph'

    assert type(test_graph) == nx.classes.multidigraph.MultiDiGraph

    nodes, edges = ox.graph_to_gdfs(test_graph)

    assert len(test_data) == len(edges), 'Failed test for create osmnx graph'

    assert nodes.index.name == 'osmid'

    assert edges.index.names == ['u','v','key']

    # Test buffer matches function
    ref = gpd.read_file('../tests/geodk_small_test.gpkg')
    osm = gpd.read_file('../tests/osm_small_test.gpkg')

    fot_id = 1095203923
    index = ref.loc[ref.fot_id==fot_id].index.values[0]
    correct_osm_matches_id = [17463, 17466, 17467, 17472, 17473, 58393, 58394]
    correct_osm_matches_ix = osm.loc[osm.osmid.isin(correct_osm_matches_id)].index.to_list()

    buffer_matches = return_buffer_matches(ref, osm, 'fot_id', 10)

    assert ['fot_id','matches_index'] == buffer_matches.columns.to_list()

    assert type(buffer_matches) == gpd.geodataframe.GeoDataFrame

    if len(buffer_matches) > 1:
        for b in buffer_matches['matches_index'].loc[index]:
            assert b in correct_osm_matches_ix

        assert len(correct_osm_matches_ix) == len(buffer_matches['matches_index'].loc[index])

    else:
        for b in buffer_matches['matches_index'].loc[0]:
            assert b in correct_osm_matches_ix

        assert len(correct_osm_matches_ix) == len(buffer_matches['matches_index'].loc[0])


    # Tests for get_segments function
    test_line = LineString([[0,0],[53,0]])
    segment_length = 8

    lines = get_segments(test_line, segment_length)

    assert len(lines.geoms) == round(test_line.length / segment_length)

    for l in lines.geoms:
        assert l.geom_type == 'LineString'

    for i in range(len(lines.geoms)-1):
        l = lines.geoms[i]
        assert l.length == segment_length

    # Test create segment gdf function
    ref = gpd.read_file('../tests/geodk_small_test.gpkg')
    seg_length = 5
    test_segments = create_segment_gdf(gdf=ref, segment_length=seg_length)
    types = list(set(test_segments.geometry.geom_type))

    assert types[0] == 'LineString'
    assert len(types) == 1

    for _, row in test_segments.iterrows():

        assert row.geometry.length <= seg_length * 1.3
        assert row.geometry.length >= seg_length / 3


    # Test find best match function
    ref = gpd.read_file('../tests/geodk_small_test.gpkg')
    osm = gpd.read_file('../tests/osm_small_test.gpkg')

    ref_segments = create_segment_gdf(ref, segment_length=5)
    osm_segments = create_segment_gdf(osm, segment_length=5)

    osm_segments['old_osmid'] = osm_segments.osmid
    osm_segments.osmid = osm_segments.seg_id
    osm_segments.drop('seg_id', axis=1, inplace=True)

    osm_segments.set_crs('EPSG:25832', inplace=True)
    ref_segments.set_crs('EPSG:25832', inplace=True)

    buffer_matches = return_buffer_matches(osm_data=osm_segments, reference_data=ref_segments, ref_id_col='seg_id', dist=10)

    matched_data = ref_segments.loc[buffer_matches.index].copy(deep=True)

    matched_data['match'] = matched_data.apply(lambda x: find_best_match(buffer_matches, ref_index=x.name, osm_edges=osm_segments, reference_edge=x['geometry'], angular_threshold=20, hausdorff_threshold=12), axis=1)

    test_values = {
        13: 114,
        14: 115,
        15: 72,
        44: 133,
        12: 113,
        22: 113,
        23: 112}

    for key, value in test_values.items():

        test_match = matched_data.loc[key, 'match']
        
        assert test_match == value, 'Unexpected match!'


    # Test find_matches_from_buffer function



