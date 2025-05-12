# %%
import matplotlib.pyplot as plt
import osmnx as ox
from cityseer.metrics import layers, networks
from cityseer.tools import graphs, io

# %%
lng, lat = 33.36402, 35.17526
buffer = 2000

poly_wgs, epsg_code = io.buffered_point_poly(lng, lat, buffer)
G = io.osm_graph_from_poly(poly_wgs, to_crs_code=3035)
G_dual = graphs.nx_to_dual(G)
nodes_gdf, _edges_gdf, network_structure = io.network_structure_from_nx(
    G_dual,
)
nodes_gdf = networks.node_centrality_simplest(
    network_structure=network_structure,
    nodes_gdf=nodes_gdf,
    distances=[1000],
)
nodes_gdf.head()

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6), facecolor="#1d1d1d")
nodes_gdf.plot(
    column="cc_harmonic_1000_ang",
    cmap="magma",
    legend=False,
    ax=ax,
)
ax.set_xlim(6433800, 6433800 + 2700)
ax.set_ylim(1669400, 1669400 + 2700)
ax.axis(False)

# %%
gdf_buildings = ox.features_from_polygon(poly_wgs, tags={"building": True})
gdf_buildings = gdf_buildings.to_crs(epsg=3035)
gdf_buildings = gdf_buildings[["building", "geometry"]]
gdf_buildings = gdf_buildings.reset_index(drop=True)
gdf_buildings["area"] = gdf_buildings.geometry.area
gdf_buildings = gdf_buildings[gdf_buildings["area"] > 10]
gdf_buildings.head()

# %%
nodes_gdf, gdf_green = layers.compute_stats(
    gdf_buildings,
    stats_column_labels=["area"],
    nodes_gdf=nodes_gdf,
    network_structure=network_structure,
    distances=[400],
)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6), facecolor="#1d1d1d")
gdf_buildings.plot(
    column="area",
    cmap="magma",
    legend=False,
    ax=ax,
)
nodes_gdf.plot(
    column="cc_area_sum_400_wt",
    cmap="magma",
    legend=False,
    ax=ax,
)
ax.set_xlim(6433800, 6433800 + 2700)
ax.set_ylim(1669400, 1669400 + 2700)
ax.axis(False)

# %%
gdf_green = ox.features_from_polygon(poly_wgs, tags={"leisure": ["park"]})
gdf_green = gdf_green.to_crs(epsg=3035)
gdf_green = gdf_green[["leisure", "geometry"]]
gdf_green = gdf_green.reset_index(drop=True)
gdf_green.head()

# %%
nodes_gdf, gdf_green = layers.compute_accessibilities(
    gdf_green,
    landuse_column_label="leisure",
    accessibility_keys=["park"],
    nodes_gdf=nodes_gdf,
    network_structure=network_structure,
    distances=[800],
)

# %%
