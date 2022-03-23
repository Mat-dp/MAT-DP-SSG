# MAT-DP Live Demo

> Display precomputed emissions data on an interactive website

> Current version only contains a Python script for extracting emissions data


## Installation

```
pip install ./path/to/repo/mat-dp-ssg
```


## Usage

```
Usage: mat-dp-ssg [OPTIONS] INPUT_CSV COUNTRY_CODE_PATH COLOUR_MAP_PATH
                  INPUT_TEMPLATE OUTPUT_FILE

Arguments:
  INPUT_CSV          An "outputs" directory containing .csv data files.
                     [required]
  COUNTRY_CODE_PATH  CSV of country codes.  [required]
  COLOUR_MAP_PATH    Map of material names to colours for graphing.
                     [required]
  INPUT_TEMPLATE     Jinja2 template file to process.  [required]
  OUTPUT_FILE        Location for processed template (will be overwritten).
                     [required]

Options:
  --preserve-zeros / --no-preserve-zeros
                                  [default: no-preserve-zeros]
  --verbose / --no-verbose        [default: no-verbose]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

Defaults for the `COUNTRY_CODE_PATH` and `COLOUR_MAP_PATH` can be found in `./defaults`.
Any colours not specified are generated randomly in the web front end.

For example:

```
poetry run mat-dp-ssg ~/some_path/E_matbytech_bycountry.csv ./defaults/country_codes.csv ./defaults/colour_map.json ./web/emissions.jinja.html ./test/out.html
```


## Building

Install the project into a python venv with

```
poetry install
```

Then you can run the development version with

```
poetry run mat-dp-ssg ...
```


## Authors
Wojciech Szwarc - data extraction script
