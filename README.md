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

`process_template.py` must be given the path to the emissions data file (`outputs/dfE_tech_bycountry.csv` from the **MAT-DP** project), and will insert appropriately formatted data into a template file (such as `test/basic.html.jinja`) and save the results to an output file.

The script is invoked as:
```
Usage: process_template.py [OPTIONS] DATA_FILE INPUT_TEMPLATE OUTPUT_FILE

Arguments:
  DATA_FILE       A .csv file containing emissions data.  [required]
  INPUT_TEMPLATE  Jinja2 template file to process.  [required]
  OUTPUT_FILE     Location for processed template (will be overwritten). [required]


Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                  Show completion for the specified shell, to copy it or customize the installation.

  --help          Show this message and exit.
```

## Authors
Wojciech Szwarc - data extraction script
