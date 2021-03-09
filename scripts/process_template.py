#!/usr/bin/env python3

import pandas as pd
import typer
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_df(file: Path):
    countries = ['UK', 'Uganda', 'KE', 'RW', 'ZA']

    df = pd.read_csv(file, index_col=0)
    df = df.drop(columns=['Hydrogen'])
    df = df.groupby(['Country', 'Scenario', 'Year']).first().loc[countries]

    # standardise naming
    df = df.rename(index=
    {
        'UK': 'United Kingdom',
        'KE': 'Kenya',
        'RW': 'Rwanda',
        'ZA': 'Zambia'
    })

    return df

def df_to_dict(df):
    if isinstance(df.index, pd.MultiIndex):
        return {name: df_to_dict(g.droplevel(0)) for name, g in df.groupby(level=0)}
    else:
        # Shape of lowest level can be tuned, see:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
        return df.to_dict('dict')


def main(data_file: Path = typer.Argument(..., help='A .csv file containing emissions data.'),
         input_template: Path = typer.Argument(..., help='Jinja2 template file to process.'),
         output_file: Path = typer.Argument(..., help='Location for processed template (will be overwritten).')):

    data_file = data_file.resolve()
    input_template = input_template.resolve()
    output_file = output_file.resolve()

    typer.echo(f'Rendering     {input_template}\nusing data in {data_file}\nand saving to {output_file}')

    df = load_df(data_file)
    env = Environment(
        loader=FileSystemLoader(input_template.parent),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(input_template.name)

    # don't use json.dumps, instead rely on Jinja doing the right thing
    stream = template.stream(plot_data=df_to_dict(df))
    with output_file.open('w') as file:
        stream.dump(file)

if __name__ == '__main__':
    typer.run(main)
