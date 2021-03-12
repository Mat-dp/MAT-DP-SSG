#!/usr/bin/env python3

import pandas as pd
import typer
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_dfs(dir: Path):

    filenames = {
        'emissions_year': 'dfE_tech_bycountry.csv',
        'emissions_mat': 'E_matbytech_bycountry.csv'
    }
    countries = ['UK', 'Uganda', 'KE', 'RW', 'ZA']

    # emissions by year
    df_ey = pd.read_csv(dir / filenames['emissions_year'], index_col=0).fillna(0)
    df_ey = df_ey.drop(columns=['Hydrogen'])
    df_ey = df_ey.groupby(['Country', 'Scenario', 'Year']).first().loc[countries]

    # emissions by mat
    df_et = pd.read_csv(dir / filenames['emissions_mat'], index_col=0).fillna(0)
    df_et = df_et.rename(columns={'tech': 'Tech'})
    df_et = df_et.groupby(['Country', 'Scenario', 'Year', 'Tech']).first().loc[countries]
    df_et = df_et.groupby(['Country', 'Scenario', 'Tech']).sum()
    df_em = df_et.groupby(['Country', 'Scenario']).sum()

    res = {
        'emissions_year': df_ey,
        'emissions_tech': df_et,
        'emissions_mat': df_em,
    }

    # standardise naming
    rename_dict = {
        'UK': 'United Kingdom',
        'KE': 'Kenya',
        'RW': 'Rwanda',
        'ZA': 'Zambia',
    }
    for name, df in res.items():
        df.rename(index=rename_dict, inplace=True)

    return res

def df_to_dict(df):
    if isinstance(df.index, pd.MultiIndex):
        return {name: df_to_dict(g.droplevel(0)) for name, g in df.groupby(level=0)}
    else:
        # Shape of lowest level can be tuned, see:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
        return df.to_dict('dict')


def main(data_dir: Path = typer.Argument(..., help='An "outputs" directory containing .csv data files.'),
         input_template: Path = typer.Argument(..., help='Jinja2 template file to process.'),
         output_file: Path = typer.Argument(..., help='Location for processed template (will be overwritten).'),
         verbose: bool = False):

    data_dir = data_dir.resolve()
    input_template = input_template.resolve()
    output_file = output_file.resolve()

    if verbose:
        typer.echo(f'Rendering     {input_template}\nusing data in {data_dir}\nand saving to {output_file}')

    env = Environment(
        loader=FileSystemLoader(input_template.parent),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(input_template.name)

    dfs = load_dfs(data_dir)

    if verbose:
        for name, df in dfs.items():
            typer.echo(f'DataFrame {name}:')
            typer.echo(df)

    # don't use json.dumps, instead rely on Jinja doing the right thing
    stream = template.stream(**{name: df_to_dict(df) for name, df in dfs.items()})
    with output_file.open('w') as file:
        stream.dump(file)

if __name__ == '__main__':
    typer.run(main)
