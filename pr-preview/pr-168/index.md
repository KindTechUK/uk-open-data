# uk-open-data

UK open data in Python for civil society, from charities and community groups
to researchers and students. Load public data from official sources, join it
to your own, and get figures you can check. The first datasets are geographic
boundaries, official statistics, postcodes and deprivation indices, with more
on the way.

## Try it now — no install

Run a real notebook in your browser. Each one fetches live ONS data through the molab cloud runtime:

<div class="grid cards" markdown>

-   __ONS statistics__

    ---

    Browse and load datasets straight from the NOMIS API.

    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/ons_statistics.py)

-   __Geographic boundaries__

    ---

    Explore LAD, LSOA and other UK boundary data interactively.

    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/geo_boundaries.py)

-   __Boundaries + statistics__

    ---

    Join geographic shapes with ONS data and map the result.

    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/geo_plus_ons.py)

</div>

## Install

Install [uk-open-data from PyPI](https://pypi.org/project/uk-open-data/):

```bash
uv add uk-open-data
```

uk-open-data depends on requests, narwhals, and python-calamine. You bring your own
DataFrame library (pandas or polars). The [package FAQ](faq/README.md) explains
which subpackages are included and how they are released.

## Quick start

```python
import pandas as pd  # or polars

from uk_open_data import (
    geodata_to_properties,
    load_geodata,
    load_ons,
    postcodes_to_geography,
)

# Local authority boundaries from the ONS Geoportal
geojson = load_geodata(geography_type="LAD", year="2025", boundary_type="BUC")
areas = pd.DataFrame(geodata_to_properties(geojson, "LAD", 2025))

# Population of each local authority from Nomis: all persons, all ages
population = load_ons(
    "population",
    geography_type="LAD",
    time="latest",
    measures=20100,
    gender=0,
    c_age=200,
    select=["geography_code", "obs_value"],
)

# Every dataset has a geography_code column, so they join directly
areas = areas.merge(population, on="geography_code")

# Your own postcodes, placed in the same local authorities
located = postcodes_to_geography(["SE13 7HX", "SE6 4RU"], geography_type="LAD")
located.merge(population, on="geography_code")
#    postcode geography_code geography_name  obs_value
# 0  SE13 7HX      E09000023       Lewisham     301037
# 1   SE6 4RU      E09000023       Lewisham     301037
```

## Bring Your Own DataFrame

uk-open-data uses [narwhals](https://narwhals-dev.github.io/narwhals/) for universal DataFrame support. The library itself has **no pandas or polars dependency** — it returns whatever backend you have installed.

```python
# With pandas installed → returns pd.DataFrame
from uk_open_data.ons import load_ons
df = load_ons("NM_1_1")
type(df)  # <class 'pandas.core.frame.DataFrame'>
```

```python
# With polars installed → returns pl.DataFrame
from uk_open_data.ons import load_ons
df = load_ons("NM_1_1")
type(df)  # <class 'polars.dataframe.frame.DataFrame'>
```

If both are installed, polars is preferred (it's faster and more memory-efficient). The geo module returns plain GeoJSON dicts — no DataFrame backend needed.

## Why does this exist?

UK public data is powerful but painful to access programmatically. The ONS ArcGIS Geoportal has no developer documentation — just a point-and-click GUI. The REST API endpoint was discovered buried in the source code of an obscure UK government R package. NOMIS is slightly better documented but requires deep knowledge of SDMX query syntax and dataset codes that aren't surfaced anywhere obvious.

Every charity, social enterprise, and researcher working with UK geographic or statistical data ends up reverse-engineering the same APIs independently. uk-open-data wraps them so you don't have to — two function calls instead of hours of documentation archaeology.

## Modules

- [**Geographic Data**](api/geo.md) — UK boundary data from ArcGIS (LAD, LSOA, etc.)
- [**ONS Statistics**](api/ons.md) — 1,615 datasets from the NOMIS API
- [**Case Studies**](case-studies/index.md) — Real-world examples from the charity sector
