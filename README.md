# Cityseer Examples

This repository contains examples for the `cityseer-api` package.

- [Main repository](https://github.com/benchmark-urbanism/cityseer-api)
- [Documentation](https://cityseer.benchmarkurbanism.com/)

## Notebooks

The following `Jupyter` notebooks provide some examples of how this package can be used.

### Getting Started Guide

The `Getting Started` guide from the [intro](https://cityseer.benchmarkurbanism.com/intro).

[getting_started](/notebooks/getting_started.ipynb)

### Graph Corrections Guide

`Graph Corrections` guide.

[graph_corrections](/notebooks/graph_corrections.ipynb)

### Graph Cleaning Guide

`Graph Cleaning` guide.

[graph_cleaning](/notebooks/graph_cleaning.ipynb)

### Importing OSM data

Examples showing how to import OSM data as discussed in [OSM and NetworkX](https://cityseer.benchmarkurbanism.com/guide).

[osm_to_cityseer](/notebooks/osm_to_cityseer.ipynb)

### Importing GeoPandas LineString data

Example showing how to import `GeoPandas` LineString data. This approach is demonstrated for ingesting a `momepy` network which can then be used for centrality and landuse accessibility analysis.

[momepy_to_cityseer](/notebooks/momepy_to_cityseer.ipynb)

### Centralities for London

Computing network centralities for London with OS Open data.

[london_centralities](/notebooks/london_centralities.ipynb)

### Landuse Accessibilities for London

Computing landuse acccessibilities to pubs and restaurants in London.

[london amenities](/notebooks/london_amenities.ipynb)

### Street Network continuity

Computing street network continuities for street names, route identifiers, and highway types:

- OS Open data: [continuity_os_open](/notebooks/continuity/continuity_os_open.ipynb)
- OSM data: [continuity_osm](/notebooks/continuity/continuity_osm.ipynb)
