#!/usr/bin/env python3

import pandas as pd
import typer
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_dfs(materials_path: Path, country_code_path: Path):
    country_codes = pd.read_csv(country_code_path)
    rename_dict = dict(zip(
        list(map(lambda x: x.strip('" '), country_codes["Alpha-2 code"])),
        list(country_codes["Country"])))

    # emissions by year
    df_ey = pd.read_csv(materials_path, index_col=0).fillna(0)
    df_ey = df_ey.groupby(['Country', 'Scenario', 'Year']).sum()
    df_ey = df_ey.stack().unstack(level='Year', fill_value=0)
    df_ey.index.set_names('Mat', -1, True)

    # emissions by mat and tech
    df_et = pd.read_csv(materials_path, index_col=0).fillna(0).rename(columns={'tech': 'Tech'})
    df_et = df_et.groupby(['Country', 'Scenario', 'Year', 'Tech']).first()
    df_em = df_et.groupby(['Country', 'Scenario']).sum()
    df_et = df_et.groupby(['Country', 'Scenario', 'Tech']).sum()
    df_et = df_et.stack().unstack(level='Tech', fill_value=0)
    df_et.index.set_names('Mat', -1, True)


    res = {
        'emissions_year': df_ey,
        'emissions_tech': df_et,
        'emissions_mat': df_em,
    }

    for name, df in res.items():
        df.rename(index=rename_dict, inplace=True)

    return res

def df_to_dict(df, drop_full_zeros = True):
    if isinstance(df.index, pd.MultiIndex):
        return {name: df_to_dict(g.droplevel(0)) for name, g in df.groupby(level=0)}
    else:
        if drop_full_zeros:
            df = df.loc[(df!=0).any(1)]
            df = df.loc[:, (df != 0).any(axis=0)]
        # Shape of lowest level can be tuned, see:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
        return df.to_dict('index')


def app(data_dir: Path = typer.Argument(..., help='An "outputs" directory containing .csv data files.'),
         input_template: Path = typer.Argument(..., help='Jinja2 template file to process.'),
         output_file: Path = typer.Argument(..., help='Location for processed template (will be overwritten).'),
         preserve_zeros: bool = False,
         verbose: bool = False):

    input_csv  = input_csv.resolve()
    input_template = input_template.resolve()
    output_file = output_file.resolve()

    if verbose:
        typer.echo(f'Rendering     {input_template}\nusing data in {input_csv}\nand saving to {output_file}')

    env = Environment(
        loader=FileSystemLoader(input_template.parent),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(input_template.name)

    dfs = load_dfs(input_csv, country_code_path)

    if verbose:
        for name, df in dfs.items():
            typer.echo(f'DataFrame {name}:')
            typer.echo(df)

    # don't use json.dumps, instead rely on Jinja doing the right thing
    stream = template.stream(**{name: df_to_dict(df, not preserve_zeros) for name, df in dfs.items()})
    with output_file.open('w') as file:
        stream.dump(file)

def main():
    typer.run(app)

if __name__ == '__main__':
    main()
