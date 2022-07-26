import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial.distance import directed_hausdorff
from shapely.ops import linemerge, substring
from shapely.geometry import LineString, MultiLineString
import osmnx as ox
import networkx as nx
import math

# TODO: Remove functions not used by current feature matching workflow

##############################

def _get_angle(linestring1, linestring2):

    # TODO: Rewrite docs

    '''
    Function for getting the smallest angle between two lines.
    Does not take the direction of lines into account: I.e. is the angle larger than 90, it is instead expressed as 180 minus the original angle.

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

def _get_hausdorff_dist(osm_edge, ref_edge):

     # TODO: Rewrite docs

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

def _get_segments(linestring, seg_length):

    '''
    Convert a Shapely LineString into segments of a speficied length.
    If a line segment ends up being shorter than the specified distance, it is merged with the segment before it.

    Arguments:
        linestring (Shapely LineString): Line to be cut into segments
        seg_length (numerical): The length of the segments

    Returns:
        lines (Shapely MultiLineString): A multilinestring consisting of the line segments.
    '''

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
    # Check that more than one line exist (to avoid cases where the line is too short to create multiple segments)
    if len(lines) > 1:
        for i, l in enumerate(lines):
            if l.length < seg_length/3:
                new_l = linemerge((lines[i-1], l))

                lines[i-1] = new_l

                del lines[i]

    lines = MultiLineString(lines)
    
    return lines


##############################

def _merge_multiline(line_geom):

    # TODO: Write docs

    # Convert a Shapely MultiLinestring into a Linestring

    if line_geom.geom_type == 'MultiLineString':
        line_geom = linemerge(line_geom)

    return line_geom

##############################

def create_segment_gdf(gdf, segment_length):

    '''
    Takes a geodataframe with linestrings and converts it into shorter segments.

    Arguments:
        gdf (geodataframe): Geodataframe with linestrings to be converted to shorter segments
        segment_length (numerical): The length of the segments

    Returns:
        segments_gdf (geodataframe): New geodataframe with segments and new unique ids (seg_id)
    '''

    gdf['geometry'] = gdf['geometry'].apply(lambda x: _merge_multiline(x))
    assert gdf.geometry.geom_type.unique()[0] == 'LineString'

    gdf['geometry'] = gdf['geometry'].apply(lambda x: _get_segments(x, segment_length))
    segments_gdf = gdf.explode(index_parts=False, ignore_index=True)

    segments_gdf.dropna(subset=['geometry'],inplace=True)

    ids = []
    for i in range(1000, 1000+len(segments_gdf)):
        ids.append(i)

    segments_gdf['seg_id'] = ids
    assert len(segments_gdf['seg_id'].unique()) == len(segments_gdf)


    return segments_gdf

##############################

def _find_matches_from_group(group_id, groups):

    # TODO: Write docs

    group = groups.get_group(group_id)

    matches = list(group.seg_id)

    return matches

##############################

def overlay_buffer(osm_data, reference_data, dist, ref_id_col):

    # TODO: write docs!

    assert osm_data.crs == reference_data.crs, 'Data not in the same crs!'

    reference_buff = reference_data[[ref_id_col, 'geometry']].copy(deep=True)
    reference_buff.geometry = reference_buff.geometry.buffer(distance=dist)

    # Overlay buffered geometries and osm segments
    joined = gpd.overlay(reference_buff, osm_data, how='intersection', keep_geom_type=False)

    # Group by id - find all matches for each ref segment
    grouped = joined.groupby(ref_id_col)

    reference_buff['matches_id'] = None

    group_ids = grouped.groups.keys()

    reference_buff['matches_id'] = reference_buff.apply(lambda x: _find_matches_from_group(x[ref_id_col], grouped) if x[ref_id_col] in group_ids else 0, axis=1)

    # Count matches
    reference_buff['count'] = reference_buff['matches_id'].apply(lambda x: len(x) if type(x) == list else 0)

    # Remove rows with no matches
    reference_buff = reference_buff[reference_buff['count'] >= 1]

    reference_buff.drop('geometry', axis=1, inplace=True)

    return reference_buff

##############################

# Function for finding the best out of potential/possible matches
def _find_best_match(buffer_matches, ref_index, osm_edges, reference_edge, angular_threshold, hausdorff_threshold):

    '''
    Finds the best match out of potential matches identifed with a buffer method. 
    Computes angle and hausdorff and find best match within threshold, if any exist.

    Arguments:
        buffer_matches(dataframe): Outcome of buffer intersection step
        ref_index: the index of the reference_edge locating it in the original dataset with reference segments
        osm_edges (geodataframe): osm_edges to be matched to the reference_edge
        reference_edge (linestring): edge currently being matched to corresponding edge in osm_edges
        angular_threshold (numerical): Threshold for max angle between lines considered a match (in degrees)
        hausdorff_threshold: Threshold for max Hausdorff distance between lines considered a match (in meters)
    
    Returns:
        best_osm_index: The index of the osm_edge identified as the best match. None if no match is found.
    '''

    #potential_matches = osm_edges[['osmid','geometry']].loc[osm_edges.osmid.isin(buffer_matches.loc[ref_index,'matches_id'])].copy(deep=True)

    potential_matches_ix = osm_edges.loc[osm_edges.seg_id.isin(buffer_matches.loc[ref_index,'matches_id'])].index

    osm_edges['angle'] = osm_edges.loc[potential_matches_ix].apply(lambda x: _get_angle(x.geometry, reference_edge), axis=1)

    # Avoid computing Hausdorff distance to edges that fail the angle threshold
    osm_edges['hausdorff_dist'] = osm_edges.loc[potential_matches_ix].apply(lambda x: _get_hausdorff_dist(osm_edge=x.geometry, ref_edge=reference_edge) if x.angle <= angular_threshold else None, axis=1)

    # Find matches within thresholds out of all matches for this referehce geometry
    potential_matches_subset = osm_edges[ (osm_edges.angle <= angular_threshold) & (osm_edges.hausdorff_dist <= hausdorff_threshold) ].copy()

    if len(potential_matches_subset) == 0:
        
        best_osm_ix = None

    elif len(potential_matches_subset) == 1:
        best_osm_ix = potential_matches_subset.index.values[0]

    else:

        # Get match(es) with smallest Hausdorff distance and angular tolerance
        potential_matches_subset['hausdorff_dist'] = pd.to_numeric(potential_matches_subset['hausdorff_dist'] )
        potential_matches_subset['angle'] = pd.to_numeric(potential_matches_subset['angle'])
        
        best_matches_index = potential_matches_subset[['hausdorff_dist','angle']].idxmin()
        best_matches = potential_matches_subset.loc[best_matches_index]
        
        best_matches = best_matches[~best_matches.index.duplicated(keep='first')] # Duplicates may appear if the same edge is the one with min dist and min angle

        if len(best_matches) == 1:

            best_osm_ix = best_matches.index.values[0]

        elif len(best_matches) > 1: # Take the one with the smallest hausdorff distance
            
            best_match_index = best_matches['hausdorff_dist'].idxmin()
            best_match = potential_matches_subset.loc[best_match_index] #.copy(deep=True)
            best_match = best_match[~best_match.index.duplicated(keep='first')]
    
            best_osm_ix = best_match.name 

    return best_osm_ix


##############################

def find_matches_from_buffer(buffer_matches, osm_edges, reference_data, angular_threshold=20, hausdorff_threshold=12):

    '''
    Finds the best/correct matches in two datasets with linestrings, from an initial matching based on a buffered intersection.

    Arguments:
        buffer_matches (dataframe): Outcome of buffer intersection step
        reference_data (geodataframe): reference data to be matched to osm data
        osm_edges (geodataframe): osm data to be matched to reference data
        angular_threshold (numerical): Threshold for max angle between lines considered a match (in degrees)
        hausdorff_threshold: Threshold for max Hausdorff distance between lines considered a match (in meters)

    Returns:
        matched_data (geodataframe): Reference data with additional columns specifying the index and ids of matched osm edges
    '''

    # Get edges matched with buffer
    matched_data = reference_data.loc[buffer_matches.index].copy(deep=True)

    # Find best match within thresholds of angles and distance
    matched_data['matches_ix'] = matched_data.apply(lambda x: _find_best_match(buffer_matches, ref_index=x.name, osm_edges=osm_edges, reference_edge=x['geometry'], angular_threshold=angular_threshold, hausdorff_threshold=hausdorff_threshold), axis=1)

    # Drop rows where no match was found
    matched_data.dropna(subset=['matches_ix'], inplace = True)

    matched_data['matches_ix'] = matched_data['matches_ix'].astype(int)
    
    ixs = matched_data['matches_ix'].values
    ids = osm_edges['seg_id'].loc[ixs].values
    matched_data['matches_id'] = ids

    print(f'{len(matched_data)} reference segments were matched to OSM edges')

    print(f'{ len(reference_data) - len(matched_data) } reference segments were not matched')

    return matched_data

##############################


def summarize_feature_matches(segments, segment_matches, seg_id_col, edge_id_col):

    # TODO: Docs!

    #Create dataframe with new and old ids and information on matches
    merged = segments.merge(segment_matches[[seg_id_col,'matches_ix','matches_id']], how ='left', on=seg_id_col)

    org_ids = list( merged[edge_id_col].unique() ) # Is edge id correct?

    matched_ids = []
    undecided_ids = []

    for i in org_ids:
        
        feature = merged.loc[merged[edge_id_col] == i].copy()

        # First check if all segments belong to the id have been matched
        if len(feature.loc[feature.matches_id.isna()]) == 0: # something like this
            # If yes, mark as matched
            matched_ids.append(i)

        else:
            # Set matched as either True or False and compute length
            feature['length'] = feature.geometry.length
            feature['matched'] = None
            
            not_matched_ix = feature.loc[feature.matches_id.isna()].index
            matched_ix = feature.loc[feature.matches_id.notna()].index
            feature.loc[not_matched_ix, 'matched'] = False
            feature.loc[matched_ix, 'matched'] = True

            summed = feature.groupby('matched').agg({'length': 'sum'})

            majority_value = summed['length'].idxmax()
            
            majority_value_len = summed.loc[majority_value].values[0]

            # If the majority value represents less than half of the edges, mark as undecided
            if majority_value_len < summed.length.sum() / 100 * 50:

                undecided_ids.append(i)

            # If more than half and true, check value to see if it is a match
            else:
                if majority_value == True:
                    matched_ids.append(i)

                else:
                    continue

    return matched_ids, undecided_ids

##############################

def update_osm(osm_segments, osm_data, final_matches, attr, unique_osm_edge_id):

    '''
    Update osm_dataset based on the attributes of the reference segments each OSM feature's segments have been matched to.

    Arguments:
        osm_segments (geodataframe): the osm_segments used in the matching process
        osm_data (geodataframe): original osm data to be updated
        final_matches (geodataframe): the result of the matching process
        attr (str): name of column in final_matches data with attribute to be transfered to osm data

    '''

    ids_attr_dict = summarize_attribute_matches(osm_segments, final_matches, attr)

    attr_df = pd.DataFrame.from_dict(ids_attr_dict, orient='index')
    attr_df.reset_index(inplace=True)
    attr_df.rename(columns={'index':'osmid',0:attr}, inplace=True)
    attr_df['osmid'] = attr_df['osmid'].astype(int)

    updated_osm = osm_data.merge(attr_df, left_on=unique_osm_edge_id, right_on='osmid', how='inner', suffixes=('','_matched'))

    return updated_osm


##############################

def summarize_attribute_matches(osm_segments, segment_matches, attr, ):

    '''
    Creates a dictionary with the original feature ids and the attribute they have been matched to

    Arguments:
        osm_segments (geodataframe): osm_segments used in the analysis
        final_matches: reference_data with information about corresponding osm segments
        attr (str): name of column in final_matches data with attribute to be transfered to osm data

    Returns:
        a dictionary with the original osmid as keys and the matched value as values
    '''

    #Create dataframe with new and old ids and information on matches

    osm_merged = osm_segments.merge(segment_matches[['seg_id',attr]],how ='left', on='seg_id', suffixes=('','_matched'))

    if attr in osm_segments.columns:
        attr = attr + '_matched'

    org_ids = list( osm_merged['osmid'].unique() )

    matched_attributes_dict = {}

    for i in org_ids:
        
        feature = osm_merged.loc[osm_merged.osmid == i].copy(deep=True)
        feature[attr] = feature[attr].fillna('none')

        matched_values = feature[attr].unique()
        if len(matched_values) == 1:
            matched_attributes_dict[str(i)] = matched_values[0]

        else:
            feature['length'] = feature.geometry.length
            summed = feature.groupby(attr).agg({'length': 'sum'})

            majority_value = summed['length'].idxmax()
            
            majority_value_len = summed.loc[majority_value].values[0]

            if majority_value_len < summed.length.sum() / 100 * 50:
                majority_value = 'undecided'

            else:
                majority_value = majority_value
            
            matched_attributes_dict[str(i)] = majority_value
        
    matched_attributes_dict = {key:val for key, val in matched_attributes_dict.items() if val != 'none'}

    return matched_attributes_dict 



##############################


#%%
if __name__ == '__main__':

    # Test merge multiline function
    line1 = LineString([[1,0],[10,0]])
    line2 = LineString([[10,0],[12,0]])
    multiline = MultiLineString([line1, line2])
    geoms = [line1, line2, multiline]
    test_gdf = gpd.GeoDataFrame(geometry=geoms)

    test_gdf['geometry'] = test_gdf['geometry'].apply(lambda x: _merge_multiline(x))

    assert test_gdf.geometry.geom_type.unique()[0] == 'LineString'

    # Test get_angle function
    linestring1 = LineString([[0,0],[10,10]])
    linestring2 = LineString([[0,0],[10,0]])
    linestring3 = LineString([[10,0],[0,0]])

    angle1 = _get_angle(linestring1, linestring2)

    angle2 = _get_angle(linestring2, linestring1)

    angle3 = _get_angle(linestring1, linestring3)

    assert round(angle1, 5) == round(angle2, 5) == round(angle3, 5), 'Angle test failed!'

    # Test get_hausdorff_dist function
    line1 = LineString([[1,1],[10,10]])
    line2 = LineString([[2,1],[4,3]])
    line3 = LineString([[4,3],[2,1]])

    h1 = _get_hausdorff_dist(line1, line2)
    h2 = _get_hausdorff_dist(line2, line1)
    h3 = _get_hausdorff_dist(line1, line3)

    h4 = LineString([[1,1],[10,1]])
    h5 = LineString([[10,1],[20,1]])
    h4 = _get_hausdorff_dist(h4, h5)

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

    # Test overlay buffer matches function
    ref = gpd.read_file('../tests/geodk_small_test.gpkg')
    osm = gpd.read_file('../tests/osm_small_test.gpkg')

    fot_id = 1095203923
    index = ref.loc[ref.fot_id==fot_id].index.values[0]
    correct_osm_matches_id = [17463, 17466, 17467, 17472, 17473, 58393, 58394]

    buffer_matches = overlay_buffer(reference_data=ref, osm_data=osm, dist=10, ref_id_col='fot_id')

    assert ['fot_id','matches_id','count'] == buffer_matches.columns.to_list()

    assert type(buffer_matches) == gpd.geodataframe.GeoDataFrame

    if len(buffer_matches) > 1:
        for b in buffer_matches['matches_id'].loc[index]:
            assert b in correct_osm_matches_id

        assert len(correct_osm_matches_id) == len(buffer_matches['matches_id'].loc[index])

    else:
        for b in buffer_matches['matches_id'].loc[0]:
            assert b in correct_osm_matches_id

        assert len(correct_osm_matches_id) == len(buffer_matches['matches_id'].loc[0])

    # Tests for get_segments function
    test_line = LineString([[0,0],[53,0]])
    segment_length = 8

    lines = _get_segments(test_line, segment_length)

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

    grouped = test_segments.groupby('fot_id')
    for n, g in grouped:
        if len(g) > 1:
            for _, row in g.iterrows():
                assert round(row.geometry.length,1) <= seg_length * 1.35 # A bit higher test value due to Shapely imprecision issues
                assert round(row.geometry.length,1) >= seg_length / 3


    # Test find best match function
    ref = gpd.read_file('../tests/geodk_small_test.gpkg')
    osm = gpd.read_file('../tests/osm_small_test.gpkg')

    ref_segments = create_segment_gdf(ref, segment_length=5)
    osm_segments = create_segment_gdf(osm, segment_length=5)

    #osm_segments['org_osmid'] = osm_segments.osmid
    # osm_segments.osmid = osm_segments.seg_id
    # osm_segments.drop('seg_id', axis=1, inplace=True)

    osm_segments.set_crs('EPSG:25832', inplace=True)
    ref_segments.set_crs('EPSG:25832', inplace=True)

    buffer_matches = overlay_buffer(osm_data=osm_segments, reference_data=ref_segments, ref_id_col='seg_id', dist=10)

    matched_data = ref_segments.loc[buffer_matches.index].copy(deep=True)

    matched_data['match'] = matched_data.apply(lambda x: _find_best_match(buffer_matches, ref_index=x.name, osm_edges=osm_segments, reference_edge=x['geometry'], angular_threshold=20, hausdorff_threshold=12), axis=1)

    # Key is ref segments index, value is osm segment index
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


    # Test find best match from buffer function
    ref_segments = gpd.read_file('../tests/ref_subset_segments.gpkg')
    osm_segments = gpd.read_file('../tests/osm_subset_segments.gpkg')

    # osm_segments['org_osmid'] = osm_segments.osmid
    # osm_segments.osmid = osm_segments.seg_id
    # osm_segments.drop('seg_id', axis=1, inplace=True)

    osm_segments.set_crs('EPSG:25832', inplace=True)
    ref_segments.set_crs('EPSG:25832', inplace=True)

    buffer_matches = overlay_buffer(osm_data=osm_segments, reference_data=ref_segments, ref_id_col='seg_id_ref', dist=10)
    final_matches = find_matches_from_buffer(buffer_matches=buffer_matches, osm_edges=osm_segments, reference_data=ref_segments, angular_threshold=20, hausdorff_threshold=15)

    # Key is ref segment id, value is osm segment id
    test_values = {
        1013: 1114,
        1014: 1115,
        1015: 1072,
        1044: 1133,
        1012: 1113,
        1022: 1113,
        1023: 1112}

    for key, value in test_values.items():

        test_match = final_matches.loc[final_matches.seg_id == key]['matches_id'].values[0]

        assert test_match == value, 'Unexpected match!'

