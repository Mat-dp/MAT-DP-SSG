# MAT-DP Live Demo

> Display precomputed emissions data on an interactive website

> Current version only contains a Python script for extracting emissions data

## Installation

In the project directory, run
```
source make-env
```
or manually execute the commands in `make-env`.

## Usage

`process_template.py` must be given the path to an output csv from the **MAT-DP** project, and will insert appropriately formatted data into a template file (such as `test/basic.html.jinja`) and save the results to an output file.

The script is invoked as:
```

Usage: process_template.py [OPTIONS] INPUT_CSV COUNTRY_CODE_PATH
                           INPUT_TEMPLATE OUTPUT_FILE

Arguments:
  INPUT_CSV          Input CSV data file  [required]
  COUNTRY_CODE_PATH  CSV of country codes  [required]
  INPUT_TEMPLATE     Jinja2 template file to process.  [required]
  OUTPUT_FILE        Location for processed template (will be overwritten).
                     [required]


Options:
  --preserve-zeros / --no-preserve-zeros
                                  [default: False]
  --verbose / --no-verbose        [default: False]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

For example:

```
./scripts/process_template.py ../MAT-DP/newoutputs/Mat_matbytech_bycountry.csv ./country_codes.csv ./web/emissions.jinja.html testout2.html
```

## Authors
Wojciech Szwarc - data extraction script
