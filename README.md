# uk-open-data

UK open data in Python for charities, researchers and students: geographic
boundaries, official statistics from the ONS and Nomis, postcode lookups and
deprivation indices for all four nations, with analyses that join them to your
own data and return figures you can check.

Made by [KindTech UK](https://github.com/KindTechUK). Up to version 0.1 the
package was called `kindtech`.

## What is in it

- **Data modules.** `uk_open_data.geo` loads boundaries from the ONS
  Geoportal, `uk_open_data.ons` loads statistics from the Nomis API,
  `uk_open_data.postcodes` turns postcodes into geography codes, and
  `uk_open_data.imd` loads the deprivation indices. Bring your own DataFrame
  backend, pandas or polars.
- **[Analyses](https://kindtechuk.github.io/uk-open-data/api/analyses/).** Each
  analysis answers one question a charity asks of its own data, such as "Are we
  reaching people in the most deprived neighbourhoods?". It returns totals,
  the working, the sources and what a person must check. Nothing in a result
  describes one person.
- **[A command line](https://kindtechuk.github.io/uk-open-data/api/cli/).**
  `uk-open-data analysis run` runs an analysis on a file without writing any
  Python.
- **[A connector for chat assistants](https://kindtechuk.github.io/uk-open-data/api/connector/).**
  The same analyses and data as tools for an assistant such as Claude or
  ChatGPT. The assistant sees totals, never rows.

These analyses follow work first done by
[DataKind UK](https://www.datakind.org.uk/) volunteers with charities.

## Installation

Install [uk-open-data from PyPI](https://pypi.org/project/uk-open-data/):

```bash
uv add uk-open-data
```

The `uk-open-data` package includes `uk_open_data.geo`, `uk_open_data.ons`,
`uk_open_data.postcodes`, and `uk_open_data.imd`. See the
[package FAQ](https://kindtechuk.github.io/uk-open-data/faq/) for how these
subpackages are installed and released together.

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

The [user guide](https://kindtechuk.github.io/uk-open-data/api/) covers each
module.

## Examples

Interactive notebooks you can run in the browser:

| Notebook | Description |
|----------|-------------|
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/ons_statistics.py) | Browse and load ONS datasets from the NOMIS API |
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/geo_boundaries.py) | Explore UK geographic boundaries |
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/geo_plus_ons.py) | Join boundaries with statistics |

### Case studies

End-to-end reproductions of [DataKind UK](https://www.datakind.org.uk/) charity
projects, each chaining several connectors on `geography_code`:

| Notebook | Case study |
|----------|------------|
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/smart_works_unemployment.py) | **Smart Works** — women's unemployment vs service reach (Census 2021 + LAD boundaries) |
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/cal_vulnerable_client.py) | **Citizens Advice Lewisham** — deprivation vs service usage (postcodes + IMD + LSOA boundaries) |
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/sobus_bame_referrals.py) | **Sobus** — BAME mental-health referrals in Hammersmith & Fulham (outcodes + Census ethnicity) |
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/starlight_play_provision.py) | **Starlight** — hospital play provision vs need across ICBs |
| [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/KindTechUK/uk-open-data/blob/main/examples/material_focus_recycling.py) | **Material Focus** — travel time to the nearest recycling point (LAD boundaries + population) |

See the [case studies](https://kindtechuk.github.io/uk-open-data/case-studies/) in
the docs for the full write-ups and figures.

## For students and researchers

The same loaders work for coursework, a dissertation or a research project that
needs UK area data. Each one fetches from the official source (the ONS
Geoportal, Nomis, postcodes.io and each nation's index of deprivation) and
returns a table with a `geography_code` column, so the sources join directly.
[Data sources](https://kindtechuk.github.io/uk-open-data/api/data-sources/)
explains the APIs behind them, and the notebooks above run in the browser with
nothing to install.

Students and researchers are welcome to contribute: a new data source, a worked
analysis, or a fix to the docs. Read the
[contributing guide](https://github.com/KindTechUK/.github/blob/main/CONTRIBUTING.md)
and [DEVELOPERS.md](https://github.com/KindTechUK/uk-open-data/blob/main/DEVELOPERS.md),
then open an [issue](https://github.com/KindTechUK/uk-open-data/issues) to say
what you would like to work on.

## Use it from an AI assistant

In Claude Code, install the plugin:

```text
/plugin marketplace add KindTechUK/plugins
/plugin install uk-open-data@kindtech
```

For other assistants, the
[connector](https://kindtechuk.github.io/uk-open-data/api/connector/) offers the
analyses and data over the Model Context Protocol. Coding agents can read the
docs as Markdown: [llms.txt](https://kindtechuk.github.io/uk-open-data/llms.txt)
lists every page, and
[llms-full.txt](https://kindtechuk.github.io/uk-open-data/llms-full.txt) holds
them all in one file.

## Development

See [DEVELOPERS.md](DEVELOPERS.md) for development setup and workflow instructions.

## Licence

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). Version 0.1.0 was
published under the MIT License; its notice is kept in NOTICE.
