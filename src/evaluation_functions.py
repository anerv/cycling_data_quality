import geopandas as gpd
import pandas as pd
import os.path


def check_settings_validity(study_area, study_area_poly_fp, study_crs, use_custom_filter, custom_filter, reference_comparison,
    reference_fp, reference_geometries, column_bidirectional):
    # Does not check for all potential errors, but givens an indication of whether settings have been filled out correctly

    assert type(study_area) == str
    assert os.path.exists(study_area_poly_fp) == True
    assert type(study_crs) == str

    if use_custom_filter == True:
        assert custom_filter != None

    if reference_comparison == True:
        assert os.path.exists(reference_fp) == True

    assert type(reference_geometries) == str
    assert type(column_bidirectional) == str


def get_graph_area(nodes, study_area_polygon, crs):

    poly = nodes.unary_union.convex_hull # Use convex hull for area computation
    poly_gdf = gpd.GeoDataFrame()
    poly_gdf.at[0,'geometry'] = poly
    poly_gdf = poly_gdf.set_crs(crs)

    area = poly_gdf.clip(study_area_polygon).area.values[0] # Clip in case convex hull goes beyond study area

    return area


def simplify_cycling_tags(osm_edges):
    # Does not take into account when there are differing types of cycling infrastructure in both sides?
        
    osm_edges['cycling_bidirectional'] = None
    osm_edges['cycling_geometries'] = None

    # Assumed to be one way if not explicitly stated that it is not
    centerline_false_bidirectional_true = ["highway == 'cycleway' & (oneway=='no' or oneway_bicycle=='no')",
                                "highway == 'bicycle_road' & (oneway =='no' or oneway_bicycle =='no')",
                                "highway == 'track' & bicycle == 'designated' & (oneway=='no' or oneway_bicycle =='no')",
                                "highway == 'path' & bicycle == 'designated' & (oneway=='no' or oneway_bicycle =='no')"]

    centerline_false_bidirectional_false = ["highway == 'cycleway' & (oneway !='no' or oneway_bicycle != 'no')",
                                "highway == 'bicycle_road' & (oneway!='no' or oneway_bicycle !='no')",
                                "highway == 'track' & bicycle == 'designated' & (oneway !='no' or oneway_bicycle !='no')",
                                "highway == 'path' & bicycle == 'designated' & (oneway !='no' or oneway_bicycle !='no')"]

    # Only cycling infrastructure in one side, but it is explicitly tagged as not oneway
    # or cycling infrastructure 
    centerline_true_bidirectional_true = ["cycleway_left in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_right in ['no','none','separate'] or cycleway_right.isnull()) and oneway_bicycle =='no'",
                                "cycleway_right in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_left in ['no','none','separate'] or cycleway_left.isnull()) and oneway_bicycle =='no'",
                                "cycleway in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (oneway_bicycle == 'no' or oneway_bicycle.isnull())",
                                "cycleway_both in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (oneway_bicycle == 'no' or oneway_bicycle.isnull())",
                                "cycleway_left in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and cycleway_right in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway']",
                                "bicycle_road =='yes' and (oneway != 'yes' or oneway_bicycle !='yes')"]

    # Only cycling infrastructure in one side and not bidirectional (if oneway_bicycle isn't explicitly yes, we assume that this type of tagging is one way)
    centerline_true_bidirectional_false = ["cycleway_left in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_right in ['no','none','separate'] or cycleway_right.isnull()) and oneway_bicycle !='no'",
                                "cycleway_right in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_left in ['no','none','separate'] or cycleway_left.isnull() ) and oneway_bicycle != 'no'",
                                "cycleway in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and oneway_bicycle == 'yes'",
                                "cycleway_both in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and oneway_bicycle == 'yes'",
                                "bicycle_road =='yes' and (oneway == 'yes' or oneway_bicycle =='yes')"]

    # The order of the queries matter: To account for instances where highway=cycleway and cycleway=some value indicating cycling infrastructure, the queries classifying based on highway should be run lastest
    for c in centerline_true_bidirectional_true:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = True
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'centerline'
    
    for c in centerline_true_bidirectional_false:
        ox_filtered = osm_edges.query(c, engine='python')
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = False
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'centerline'

    
    for c in centerline_false_bidirectional_true:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = True
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'true_geometries'

    for c in centerline_false_bidirectional_false:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = False
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'true_geometries'


    # Assert that cycling bidirectional and cycling geometries have been filled out for all where cycling infrastructure is yes!
    assert len(osm_edges.query("cycling_infrastructure =='yes' & (cycling_bidirectional.isnull() or cycling_geometries.isnull())")) == 0, 'Not all cycling infrastructure has been classified!'

    print(osm_edges.cycling_bidirectional.value_counts())
    print(osm_edges.cycling_geometries.value_counts())

    return osm_edges


def measure_infrastructure_length(edge, geometry_type, bidirectional, cycling_infrastructure):

    edge_length = edge.length

    # TODO: Simplify - only need cycling infrastructure and bidirectional?

    if cycling_infrastructure == 'yes' and geometry_type == 'true_geometries' and bidirectional == True:
        infrastructure_length = edge_length * 2
      
    elif cycling_infrastructure == 'yes' and geometry_type == 'true_geometries' and bidirectional == False:
        infrastructure_length = edge_length
     
    elif cycling_infrastructure == 'yes' and geometry_type == 'centerline' and bidirectional == True:
        infrastructure_length = edge_length * 2
       
    elif cycling_infrastructure == 'yes' and geometry_type == 'centerline' and bidirectional == False:
        infrastructure_length = edge_length
        
 
    elif cycling_infrastructure == 'yes' and (geometry_type is None or bidirectional is None):
        print('Missing information when calculating true infrastructure length!')
        infrastructure_length = None
    
    else:
        infrastructure_length = None

    return infrastructure_length


def create_cycling_network(new_edges, original_nodes, original_graph, return_nodes=False):
    # Create new OSMnx graph from a subset of edges of a larger graph

    #Getting a list of unique nodes used by bike_edges
    new_edges_index = pd.MultiIndex.to_frame(new_edges.index)
    u = new_edges_index['u'].to_list()
    v = new_edges_index['v'].to_list()

    used_nodes = list(set().union(u,v))

    #All nodes are copied to an new dataframe
    new_nodes = original_nodes.copy(deep=True)

    #Creating new column in bike_nodes with the index value
    new_nodes['osmid'] = new_nodes.index

    #Using list of nodes to mask out unnecessary nodes
    new_nodes = new_nodes[new_nodes['osmid'].isin(used_nodes)]

    #Drop column - not needed anymore 
    new_nodes.drop(columns='osmid', inplace=True)

    #Create graph from nodes and edge geodataframe
    new_graph = ox.graph_from_gdfs(new_nodes, new_edges, graph_attrs=original_graph.graph)

    if return_nodes:
        return new_graph, new_nodes
    
    else:
        return new_graph