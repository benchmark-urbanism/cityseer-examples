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
    distances=[500, 1000, 2000, 5000],
)
nodes_gdf.head()

# %%
gdf_restraunts = ox.features_from_polygon(poly_wgs, tags={"amenity": "restaurant"})
gdf_restraunts = gdf_restraunts.to_crs(epsg=3035)
gdf_restraunts = gdf_restraunts[["amenity", "geometry"]]
gdf_restraunts = gdf_restraunts.reset_index(drop=True)
gdf_restraunts.head()

# %%
nodes_gdf, gdf_restraunts = layers.compute_accessibilities(
    gdf_restraunts,
    landuse_column_label="amenity",
    accessibility_keys=["restaurant"],
    nodes_gdf=nodes_gdf,
    network_structure=network_structure,
    distances=[200, 400, 800],
)

# %%
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(
    nodes_gdf[
        [
            "cc_density_500_ang",
            "cc_density_1000_ang",
            "cc_density_2000_ang",
            "cc_density_5000_ang",
            "cc_harmonic_500_ang",
            "cc_harmonic_1000_ang",
            "cc_harmonic_2000_ang",
            "cc_harmonic_5000_ang",
            "cc_betweenness_500_ang",
            "cc_betweenness_1000_ang",
            "cc_betweenness_2000_ang",
            "cc_betweenness_5000_ang",
        ]
    ]
)

# Perform PCA
pca = PCA(n_components=4)
X_pca = pca.fit_transform(X_scaled)

# Add PCA components to the DataFrame
nodes_gdf["pca_1"] = X_pca[:, 0]
nodes_gdf["pca_2"] = X_pca[:, 1]
nodes_gdf["pca_3"] = X_pca[:, 2]
nodes_gdf["pca_4"] = X_pca[:, 3]

# plot explained variance
fig, ax = plt.subplots(2, 1, figsize=(8, 10), facecolor="#1d1d1d")
nodes_gdf.plot(
    column="pca_1",
    cmap="magma",
    legend=False,
    ax=ax[0],
)
ax[0].set_xlim(6433800, 6433800 + 2700)
ax[0].set_ylim(1669400, 1669400 + 2700)
ax[0].axis(False)
ax[0].set_title(
    "PCA 1 - explained variance: {:.0%}".format(pca.explained_variance_ratio_[0])
)

nodes_gdf.plot(
    column="pca_2",
    cmap="magma",
    legend=False,
    ax=ax[1],
)
ax[1].set_xlim(6433800, 6433800 + 2700)
ax[1].set_ylim(1669400, 1669400 + 2700)
ax[1].axis(False)
ax[1].set_title(
    "PCA 2 - explained variance: {:.0%}".format(pca.explained_variance_ratio_[1])
)

# %%
# seaborn scatterplot with hexbin
import seaborn as sns

sns.jointplot(
    data=nodes_gdf,
    x="pca_1",
    y="cc_restaurant_800_wt",
    cmap="magma",
    kind="kde",
    ax=ax,
)

# %%
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

X = nodes_gdf[["pca_1", "pca_2", "pca_3", "pca_4"]]
y = nodes_gdf["cc_restaurant_800_wt"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
regressor = RandomForestRegressor(
    n_estimators=100, random_state=42, criterion="squared_error"
)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)

# R2 score
r2 = r2_score(y_test, y_pred)
print("R2 score: ", r2)

# plot residuals
nodes_gdf["cc_restaurant_800_wt_pred"] = regressor.predict(X)
nodes_gdf["cc_restaurant_800_residuals"] = (
    nodes_gdf["cc_restaurant_800_wt_pred"] - nodes_gdf["cc_restaurant_800_wt"]
)

fig, ax = plt.subplots(3, 1, figsize=(8, 12), facecolor="#1d1d1d")
nodes_gdf.plot(
    column="cc_restaurant_800_wt",
    cmap="magma",
    legend=True,
    ax=ax[0],
)
ax[0].set_xlim(6433800, 6433800 + 2700)
ax[0].set_ylim(1669400, 1669400 + 2700)
ax[0].axis(False)
ax[0].set_title("Restaurant Accessibility")

nodes_gdf.plot(
    column="cc_restaurant_800_wt_pred",
    cmap="magma",
    legend=True,
    ax=ax[1],
)
ax[1].set_xlim(6433800, 6433800 + 2700)
ax[1].set_ylim(1669400, 1669400 + 2700)
ax[1].axis(False)
ax[1].set_title("Predicted Restaurant Accessibility - R2 score: {:.2f}".format(r2))

nodes_gdf.plot(
    column="cc_restaurant_800_residuals",
    cmap="coolwarm",
    vmax=4,
    vmin=-4,
    legend=True,
    ax=ax[2],
)
ax[2].set_xlim(6433800, 6433800 + 2700)
ax[2].set_ylim(1669400, 1669400 + 2700)
ax[2].axis(False)
ax[2].set_title("Residuals of Random Forest Regression")
plt.tight_layout()

# %%
