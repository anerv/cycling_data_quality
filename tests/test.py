#%%
import geopandas as gpd
import pandas as pd
import os.path
import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon, Point
import math

from src import evaluation_functions as ef
from src import styling_functions as sf
#%%
###################### TESTS FOR EVALUATION FUNCTIONS #############################





# Test for fix_key_index
l1 = LineString([[1,1],[10,10]])
l2 = LineString([[2,1],[6,10]])
l3 = LineString([[10,10],[10,20]])
l4 = LineString([[11,9],[5,20]])
l5 = LineString([[1,12],[4,12]])
l6 = LineString([[11,9],[5,20]])

lines = [l1, l2, l3,l4,l5,l6]
# Correct, key values should not be modified
u = [1,2,3,4,2,1]
v = [2,3,4,1,3,2]
key = [0,0,0,0,1,1]

d = {'u':u,'v':v,'key':key, 'geometry':lines }
edges = gpd.GeoDataFrame(d)
edges.set_index(['u','v','key'],inplace=True)

edges_test = ef.fix_key_index(edges)

assert list(edges_test.reset_index()['key'].values) == key
assert len(edges) == len(edges_test)

# Incorrect, key values should be modified
u = [1,2,3,4,5,6]
v = [2,3,4,1,3,2]
key = [0,0,0,0,1,1]

d = {'u':u,'v':v,'key':key, 'geometry':lines }
edges = gpd.GeoDataFrame(d)
edges.set_index(['u','v','key'],inplace=True)

edges_test = ef.fix_key_index(edges)

assert list(edges_test.reset_index()['key'].values) != key
k = list(edges_test.reset_index()['key'].values)
assert k[-1] == 0
assert k[-2] == 0
assert len(edges) == len(edges_test)





# Test for find pct difference
d={'col1':[10,20,105,40,100],'col2':[10,40,100,4,90]}
df = pd.DataFrame(d)

df['pct_difference'] = df.apply( lambda x: ef.find_pct_diff(x, 'col1', 'col2'), axis=1)

assert df['pct_difference'].values[0] == 0.00
assert df['pct_difference'].values[1] == -66.67
assert df['pct_difference'].values[2] == 4.88
assert df['pct_difference'].values[3] == 163.64
assert df['pct_difference'].values[4] == 10.53

d={'col1':[10,20,105,40,np.nan],'col2':[10,40,100,4,90]}
df = pd.DataFrame(d)

df['pct_difference'] = df.apply( lambda x: ef.find_pct_diff(x, 'col1', 'col2'), axis=1)
assert math.isnan(df.loc[4,'pct_difference']) == True





# Test for create_grid_geometry 
ext = [(0,0),(0,10),(10,10),(10,0)]
interior = [(4,4),(6,4),(6,6),(4,6)]
poly = Polygon(ext, [interior])
gdf = gpd.GeoDataFrame(geometry=[poly])
grid = ef.create_grid_geometry(gdf, 1)

assert len(grid) == (10*10) - (2*2)
assert len(grid.geom_type.unique()) == 1
assert grid.geom_type.unique()[0] == 'Polygon'
assert grid.loc[0,'geometry'].area == 1






# Test simplify cycling tags
l1 = LineString([[1,1],[10,10]])
l2 = LineString([[2,1],[6,10]])
l3 = LineString([[10,10],[10,20]])
l4 = LineString([[11,9],[5,20]])
l5 = LineString([[1,12],[4,12]])

lines = [l1, l2, l3,l4,l5]
d = {'highway': ['cycleway','primary','secondary','path','track'],
    'cycling_infrastructure': ['yes','yes','yes','yes','yes'],
    'cycleway': [np.nan,'track',np.nan,np.nan,'no'],
    'cycleway_both': [np.nan,np.nan,'shared_lane','track',np.nan],
    'bicycle_road': [0,0,0,0,'yes'],
    'bicycle': [np.nan,np.nan,np.nan,'designated','designated'],
    'cycleway_right': [np.nan,np.nan,np.nan,np.nan,np.nan],
    'cycleway_left': [np.nan,np.nan,np.nan,np.nan,np.nan],
    'oneway': ['no','yes',np.nan,'yes',np.nan],
    'oneway_bicycle': [np.nan,'yes',np.nan, 'no',np.nan],
    'geometry':lines }
edges = gpd.GeoDataFrame(d)
edges['length'] = edges.geometry.length

edges = ef.simplify_cycling_tags(edges)

assert edges.loc[0,'cycling_bidirectional'] == True and edges.loc[0,'cycling_geometries'] == 'true_geometries'
assert edges.loc[1,'cycling_bidirectional'] == False and edges.loc[1,'cycling_geometries'] == 'centerline'
assert edges.loc[2,'cycling_bidirectional'] == True and edges.loc[2,'cycling_geometries'] == 'centerline'
assert edges.loc[3,'cycling_bidirectional'] == True and edges.loc[3,'cycling_geometries'] == 'true_geometries'
assert edges.loc[4,'cycling_bidirectional'] == False and edges.loc[4,'cycling_geometries'] == 'true_geometries'



# Test measure_infrastructure_length
l1 = LineString([[1,1],[10,10]])
l2 = LineString([[2,1],[6,10]])
l3 = LineString([[10,10],[10,20]])
l4 = LineString([[11,9],[5,20]])
l5 = LineString([[1,12],[4,12]])

lines = [l1, l2, l3,l4,l5]
d = {'cycling_infrastructure': ['yes','yes','yes','yes','no'],
    'cycling_bidirectional': [True,False,False,True,False],
    'cycling_geometries': ['true_geometries','true_geometries','centerline','centerline','centerline'],
    'geometry':lines }
edges = gpd.GeoDataFrame(d)
edges['length'] = edges.geometry.length


edges['infrastructure_length'] = edges.apply(lambda x: ef.measure_infrastructure_length(edge = x.geometry, 
                                                    geometry_type=x.cycling_geometries, bidirectional=x.cycling_bidirectional, cycling_infrastructure=x.cycling_infrastructure), axis=1)


assert edges.loc[0,'infrastructure_length'] == edges.loc[0,'length'] * 2
assert edges.loc[1,'infrastructure_length'] == edges.loc[1,'length']
assert edges.loc[2,'infrastructure_length'] == edges.loc[2,'length']
assert edges.loc[3,'infrastructure_length'] == edges.loc[3,'length'] * 2
assert pd.isnull(edges.loc[4,'infrastructure_length']) == True




# Test define_protected_unprotected
l1 = LineString([[1,1],[10,10]])
l2 = LineString([[2,1],[6,10]])
l3 = LineString([[10,10],[10,20]])
l4 = LineString([[11,9],[5,20]])
l5 = LineString([[1,12],[4,12]])

lines = [l1, l2, l3,l4,l5]
d = {'highway': ['cycleway','primary','secondary','path','track'],
    'cycleway': [np.nan,'track',np.nan,'lane','no'],
    'cycleway_both': [np.nan,np.nan,'shared_lane','track',np.nan],
    'bicycle_road': [0,0,0,0,'yes'],
    'cycleway_right': [np.nan,np.nan,np.nan,np.nan,np.nan],
    'cycleway_left': [np.nan,np.nan,np.nan,np.nan,np.nan],
    'geometry':lines }
edges = gpd.GeoDataFrame(d)
edges['length'] = edges.geometry.length


queries = {'protected': ["highway == 'cycleway'",
"cycleway in ['track','opposite_track']",
"cycleway_left in ['track','opposite_track']",
"cycleway_right in ['track','opposite_track']",
"cycleway_both in ['track','opposite_track']"],
'unprotected': ["cycleway in ['lane','opposite_lane','shared_lane','crossing']",
"cycleway_left in ['lane','opposite_lane','shared_lane','crossing']",
"cycleway_right in ['lane','opposite_lane','shared_lane','crossing']",
"cycleway_both in ['lane','opposite_lane','shared_lane','crossing']",
"bicycle_road == 'yes'"],
'unknown': ["cycleway in ['designated']",
"cycleway_left in ['designated']",
"cycleway_right in ['designated']",
"cycleway_both in ['designated']"]}

edges = ef.define_protected_unprotected(edges,queries)

assert edges.loc[0, 'protected'] == 'protected'
assert edges.loc[1, 'protected'] == 'protected'
assert edges.loc[2, 'protected'] == 'unprotected'
assert edges.loc[3, 'protected'] == 'mixed'
assert edges.loc[4, 'protected'] == 'unprotected'





# Test get_dangling_nodes
edges = gpd.read_file('../tests/edges.gpkg')
nodes = gpd.read_file('../tests/nodes.gpkg')
nodes.set_index('osmid',inplace=True)

d_nodes = ef.get_dangling_nodes(edges, nodes)
assert len(d_nodes) == 9
assert type(d_nodes) == gpd.geodataframe.GeoDataFrame




# Test count features in grid
ext = [(0,0),(0,10),(10,10),(10,0)]
interior = [(4,4),(6,4),(6,6),(4,6)]
poly = Polygon(ext, [interior])
gdf = gpd.GeoDataFrame(geometry=[poly])
grid = ef.create_grid_geometry(gdf, 1)
grid['grid_id'] = grid.index

points = gpd.read_file('../tests/random_points.gpkg')
points_joined = gpd.overlay(points, grid, how ='intersection')

test_count = ef.count_features_in_grid(points_joined, 'points')

assert test_count.loc[0,'count_points'] == 2
assert test_count.loc[18,'count_points'] == 2
assert test_count.loc[28,'count_points'] == 1



# Test length of features in grid
ext = [(0,0),(0,10),(10,10),(10,0)]
poly = Polygon(ext)
gdf = gpd.GeoDataFrame(geometry=[poly])
grid = ef.create_grid_geometry(gdf, 1)
grid['grid_id'] = grid.index

# Test length_of_features_in_grid
line_gdf = gpd.read_file('../tests/random_lines.gpkg',driver='GPKG')
lines_joined = gpd.overlay(line_gdf, grid, how ='intersection', keep_geom_type=True)

test_length = ef.length_of_features_in_grid(lines_joined, 'lines')

assert round(test_length.loc[0,'length_lines'],2) == 1.41
assert round(test_length.loc[1,'length_lines'],2) == 2.83





# Test check_intersection
l1 = LineString([[1,1],[10,10]])
l2 = LineString([[2,1],[6,10]])
l3 = LineString([[10,10],[10,20]])
l4 = LineString([[11,9],[5,20]])
l5 = LineString([[1,12],[4,12]])

lines = [l1, l2, l3,l4,l5]
d = {'bridge':['yes','no', None,'no',None],'tunnel':['no','no',None,None,None], 'geometry':lines }
edges = gpd.GeoDataFrame(d)

edges['intersection_issues'] = edges.apply(lambda x: ef.check_intersection(row = x, gdf=edges, print_check=False), axis=1)

count_intersection_issues = len(edges.loc[(edges.intersection_issues.notna()) & edges.intersection_issues > 0])

assert count_intersection_issues == 2
assert edges.loc[2,'intersection_issues'] == 1
assert edges.loc[3,'intersection_issues'] == 1






# Test incompatible tags
l1 = LineString([[1,1],[10,10]])
l2 = LineString([[2,1],[6,10]])
l3 = LineString([[10,10],[10,20]])
l4 = LineString([[11,9],[5,20]])
l5 = LineString([[1,12],[4,12]])

lines = [l1, l2, l3,l4,l5]
d = {'cycling':['yes','no', None,'yes',None],'car':['no','no',None,'yes',None], 'geometry':lines }
edges = gpd.GeoDataFrame(d)

dict = {'cycling': {'yes': [['bicycle', 'no'],
['bicycle', 'dismount'],
['car', 'yes']]}}

incomp_tags_results = ef.check_incompatible_tags(edges, dict)
assert incomp_tags_results['cycling/car'] == 1





# Test missing tags
l1 = LineString([[1,1],[10,10]])
l2 = LineString([[2,1],[6,10]])
l3 = LineString([[10,10],[10,20]])
l4 = LineString([[11,9],[5,20]])
l5 = LineString([[1,12],[4,12]])

lines = [l1, l2, l3,l4,l5]
d = {'cycleway_width': [np.nan,2,2,1,np.nan],'width':[1,np.nan,2,1,0], 
    'surface':['paved', np.nan, np.nan, 'gravel',np.nan], 
    'cycling_geometries': ['true_geometries','true_geometries','centerline','centerline','centerline'],
    'geometry':lines }
edges = gpd.GeoDataFrame(d)

dict = {'surface': {'true_geometries': ['surface', 'cycleway_surface'],
'centerline': ['cycleway_surface']},
'width': {'true_geometries': ['width',
'cycleway_width',
'cycleway_left_width',
'cycleway_right_width',
'cycleway_both_width'],
'centerline': ['cycleway_width',
'cycleway_left_width',
'cycleway_right_width',
'cycleway_both_width']},
'speedlimit': {'all': ['maxspeed']},
'lit': {'all': ['lit']}}

existing_tags_results = ef.analyse_missing_tags(edges, dict)
assert existing_tags_results['surface'] == 1
assert existing_tags_results['width'] == 4





# Test find_network_gaps
G = nx.MultiDiGraph() # construct the graph
G.add_node(1, x=10, y=10)
G.add_node(2, x=20, y=20)
G.add_node(3, x=25, y=30)
G.add_node(4, x=25, y=40)
G.add_node(5, x=24, y=40)

# add length and osmid just for the osmnx function to work
G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

G.graph['crs'] = 'epsg:25832'
nodes, edges = ox.graph_to_gdfs(G)

test_gaps = ef.find_network_gaps(nodes, edges, 1)
assert len(test_gaps) == 1
assert test_gaps[0][0] == 4
assert test_gaps[0][1] == 5





# Test component_lengths
G = nx.MultiDiGraph()
# One component
G.add_node(1, x=10, y=10)
G.add_node(2, x=20, y=20)
G.add_node(3, x=25, y=30)
G.add_node(4, x=25, y=40)
G.add_node(5, x=24, y=40)

# add length and osmid just for the functions to work
G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

# Second component
G.add_node(6, x=50, y=50)
G.add_node(7, x=47, y=47)
G.add_node(8, x=53, y=50)
G.add_node(9, x=45, y=60)
G.add_node(10, x=44, y=60)

# add length and osmid just for the functions to work
G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

G.graph['crs'] = 'epsg:25832'
nodes, edges = ox.graph_to_gdfs(G)

components = ef.return_components(G)
test_c_lengths = ef.component_lengths(components)

assert test_c_lengths.loc[0,'component_length'] == 40
assert test_c_lengths.loc[1,'component_length'] == 67







# Test find_adjacent_components
G = nx.MultiDiGraph()
# One component
G.add_node(1, x=10, y=10)
G.add_node(2, x=20, y=20)
G.add_node(3, x=25, y=30)
G.add_node(4, x=25, y=40)
G.add_node(5, x=24, y=40)

# add length and osmid just for the functions to work
G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

# Second component
G.add_node(6, x=50, y=50)
G.add_node(7, x=47, y=47)
G.add_node(8, x=53, y=50)
G.add_node(9, x=45, y=60)
G.add_node(10, x=44, y=60)

G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

# Third component
G.add_node(11, x=53, y=55)
G.add_node(12, x=70, y=70)
G.add_node(13, x=80, y=85)
G.add_node(14, x=75, y=85)

G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

G.graph['crs'] = 'EPSG:25832'
nodes, edges = ox.graph_to_gdfs(G)

components = ef.return_components(G)
adj_comps = ef.find_adjacent_components(components,buffer_dist=5, crs='EPSG:25832')

assert adj_comps.loc[0,'component'] == 1
assert adj_comps.loc[1,'component'] == 2
assert len(adj_comps) == 2
assert adj_comps.loc[0,'from'] == 8 and adj_comps.loc[0,'to'] == 9
assert adj_comps.loc[1,'from'] == 11 and adj_comps.loc[1,'to'] == 12






# Test assign_component_id
G = nx.MultiDiGraph()
# One component
G.add_node(1, x=10, y=10)
G.add_node(2, x=20, y=20)
G.add_node(3, x=25, y=30)
G.add_node(4, x=25, y=40)
G.add_node(5, x=24, y=40)

# add length and osmid just for the functions to work
G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

# Second component
G.add_node(6, x=50, y=50)
G.add_node(7, x=47, y=47)
G.add_node(8, x=53, y=50)
G.add_node(9, x=45, y=60)
G.add_node(10, x=44, y=60)

G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

# Third component
G.add_node(11, x=53, y=55)
G.add_node(12, x=70, y=70)
G.add_node(13, x=80, y=85)
G.add_node(14, x=75, y=85)

G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

G.graph['crs'] = 'EPSG:25832'
nodes, edges = ox.graph_to_gdfs(G)
edges['edge_id'] = edges['osmid']

components = ef.return_components(G)
edges_comp_ids, comp_dict = ef.assign_component_id(components, edges, edge_id_col='osmid')

assert len(edges_comp_ids) == 11
assert len(comp_dict) == 3
assert list(comp_dict.keys()) == [0,1,2]
assert edges_comp_ids[0:4]['component'].unique()[0] == 0
assert edges_comp_ids[4:8]['component'].unique()[0] == 1
assert edges_comp_ids[8:10]['component'].unique()[0] ==2




# Test assign_component_id_to_grid
G = nx.MultiDiGraph()
# One component
G.add_node(1, x=10, y=10)
G.add_node(2, x=20, y=20)
G.add_node(3, x=25, y=30)
G.add_node(4, x=25, y=40)
G.add_node(5, x=24, y=40)

# add length and osmid just for the functions to work
G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

# Second component
G.add_node(6, x=50, y=50)
G.add_node(7, x=47, y=47)
G.add_node(8, x=53, y=50)
G.add_node(9, x=45, y=60)
G.add_node(10, x=44, y=60)

G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

# Third component
G.add_node(11, x=53, y=55)
G.add_node(12, x=70, y=70)
G.add_node(13, x=80, y=85)
G.add_node(14, x=75, y=85)

G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

G.graph['crs'] = 'EPSG:25832'
nodes, edges = ox.graph_to_gdfs(G)
edges['edge_id'] = edges['osmid']

components = ef.return_components(G)
edges_comp_ids, comp_dict = ef.assign_component_id(components, edges, edge_id_col='osmid')

# Create test grid and joined data
grid = gpd.read_file('../tests/grid_component_test.gpkg',driver='GPKG')
edges_joined = gpd.overlay(edges, grid, how ='intersection', keep_geom_type=True)

test_id_to_grid = ef.assign_component_id_to_grid(simplified_edges=edges, edges_joined_to_grids=edges_joined, components=components, grid=grid, prefix='osm', edge_id_col='osmid')

assert len(test_id_to_grid) == len(grid)
assert test_id_to_grid.loc[5,'component_ids_osm'][0] == 0
assert test_id_to_grid.loc[7,'component_ids_osm'][0] == 0
assert test_id_to_grid.loc[14,'component_ids_osm'][0] == 0
assert test_id_to_grid.loc[26,'component_ids_osm'][0] == 1
assert test_id_to_grid.loc[27,'component_ids_osm'][0] == 1
assert test_id_to_grid.loc[28,'component_ids_osm'][0] == 1
assert test_id_to_grid.loc[35,'component_ids_osm'][0] == 1
assert test_id_to_grid.loc[35,'component_ids_osm'][1] == 2
assert test_id_to_grid.loc[48,'component_ids_osm'][0] == 2
assert test_id_to_grid.loc[49,'component_ids_osm'][0] == 2






# Test count_component_cell_reach
G = nx.MultiDiGraph()
# One component
G.add_node(1, x=10, y=10)
G.add_node(2, x=20, y=20)
G.add_node(3, x=25, y=30)
G.add_node(4, x=25, y=40)
G.add_node(5, x=24, y=40)

# add length and osmid just for the functions to work
G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

# Second component
G.add_node(6, x=50, y=50)
G.add_node(7, x=47, y=47)
G.add_node(8, x=53, y=50)
G.add_node(9, x=45, y=60)
G.add_node(10, x=44, y=60)

G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

# Third component
G.add_node(11, x=53, y=55)
G.add_node(12, x=70, y=70)
G.add_node(13, x=80, y=85)
G.add_node(14, x=75, y=85)

G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

G.graph['crs'] = 'EPSG:25832'
nodes, edges = ox.graph_to_gdfs(G)
edges['edge_id'] = edges['osmid']

components = ef.return_components(G)

components_df = ef.component_lengths(components)

# Create test grid and joined data
grid = gpd.read_file('../tests/grid_component_test.gpkg',driver='GPKG')

edges_joined = gpd.overlay(edges, grid, how ='intersection', keep_geom_type=True)
grid = ef.assign_component_id_to_grid(simplified_edges=edges, edges_joined_to_grids=edges_joined, components=components, grid=grid, prefix='osm', edge_id_col='osmid')

test_comp_cell_reach = ef.count_component_cell_reach(components_df, grid, 'component_ids_osm')

assert len(test_comp_cell_reach) == len(components)
assert list(test_comp_cell_reach.keys()) == components_df.index.to_list()
assert test_comp_cell_reach[0] == 6
assert test_comp_cell_reach[1] == 4
assert test_comp_cell_reach[2] == 6


#%%
###############################
# Test find_overshoots function
G = nx.MultiDiGraph() # construct the graph
G.add_node(1, x=10, y=10)
G.add_node(2, x=20, y=20)
G.add_node(3, x=25, y=30)
G.add_node(4, x=25, y=28)
G.add_node(5, x=20, y=15)

# add length and osmid just for the osmnx function to work
G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
G.add_edge(3, 4, 0, length=2, osmid=np.random.randint(1, 999999))
G.add_edge(2, 5, 0, length=5, osmid=np.random.randint(1, 999999))

G.graph['crs'] = 'epsg:25832'
nodes, edges = ox.graph_to_gdfs(G)
edges['length'] = edges.geometry.length
dn_nodes = get_dangling_nodes(edges, nodes)

overshoots_2 = find_overshoots(dn_nodes, edges, 2)
overshoots_5 = find_overshoots(dn_nodes, edges, 5)

assert len(overshoots_2) == 1
assert len(overshoots_5) == 2
assert overshoots_2['u'].values[0] == 3
assert overshoots_2['v'].values[0] == 4
assert overshoots_5['u'].values[0] == 2
assert overshoots_5['v'].values[0] == 5
assert overshoots_5['u'].values[1] == 3
assert overshoots_5['v'].values[1] == 4

# Test find_undershoots function
G = nx.MultiDiGraph() # construct the graph
G.add_node(1, x=1, y=1)
G.add_node(2, x=1, y=20)
G.add_node(3, x=1, y=30)
G.add_node(4, x=10, y=20)
G.add_node(5, x=20, y=20)
G.add_node(6, x=12, y=18)
G.add_node(7, x=12, y=1)
G.add_node(8, x=5, y=18)
G.add_node(9, x=5, y=1)
G.add_node(10, x=20, y=22)


# add length and osmid just for the osmnx function to work
G.add_edge(1, 2, 0, length=10, osmid=12)
G.add_edge(2, 3, 0, length=10, osmid=23)
G.add_edge(2, 4, 0, length=5, osmid=24)
G.add_edge(4, 5, 0, length=2, osmid=45)
G.add_edge(4, 6, 0, length=2, osmid=46)
G.add_edge(6, 7, 0, length=2, osmid=67)
G.add_edge(8, 9, 0, length=2, osmid=89)
G.add_edge(5, 10, 0, length=2, osmid=510)

G.graph['crs'] = 'epsg:25832'

nodes, edges = ox.graph_to_gdfs(G)
edges['length'] = edges.geometry.length
edges['edge_id'] = edges.osmid
dangling_nodes = get_dangling_nodes(edges, nodes)

undershoot_dict_3, undershoot_nodes_3 = find_undershoots(dangling_nodes, edges, 3, 'edge_id')

undershoot_dict_5, undershoot_nodes_5 = find_undershoots(dangling_nodes, edges, 5, 'edge_id')

assert len(undershoot_dict_3) == 1
assert len(undershoot_dict_5) == 3
assert list(undershoot_dict_3.keys()) == [8]
assert list(undershoot_dict_3.values()) == [[24]]

assert list(undershoot_dict_5.keys()) == [1,8,9]
assert list(undershoot_dict_5.values()) == [[89], [12, 24, 23], [12]]