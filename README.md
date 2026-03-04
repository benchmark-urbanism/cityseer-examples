# Cityseer Guide

Published to: [Cityseer Guide](https://benchmark-urbanism.github.io/cityseer-examples/)

Tutorials and worked examples for [`cityseer`](https://github.com/benchmark-urbanism/cityseer-api), a Python package for pedestrian-scale network analysis and urban morphology.

## Contents

- **[Python 101](https://benchmark-urbanism.github.io/cityseer-examples/class/index.html):** Introduction to Python, spatial data, GeoPandas, and urban analytics for beginners.
- **[Cityseer Recipes](https://benchmark-urbanism.github.io/cityseer-examples/recipes/index.html):** Practical notebooks covering network preparation, centrality, accessibility, statistics, visibility, and continuity analysis.
- **[Glossary](https://benchmark-urbanism.github.io/cityseer-examples/glossary.html):** Definitions of key terms (primal/dual graphs, edge rolloff, network distance, etc.).
- **[Datasets](https://benchmark-urbanism.github.io/cityseer-examples/data/datasets.html):** Source data used in the recipes, with licensing and column descriptions.

## Related

- [cityseer API documentation](https://cityseer.benchmarkurbanism.com/)
- [cityseer repository](https://github.com/benchmark-urbanism/cityseer-api)

## Development

Requires [uv](https://docs.astral.sh/uv/) and [Quarto](https://quarto.org/):

```bash
brew install uv quarto
uv sync
```

Preview the site locally:

```bash
quarto preview
```

The VS Code [Quarto extension](https://marketplace.visualstudio.com/items?itemName=quarto.quarto) is recommended for editing `.qmd` files.

## License

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
