#!/usr/bin/env python3
# stats.py
# github.com/deadbits/prompt-serve
# collect statistics from prompt-serve yaml files

import os
import sys
import yaml
import pandas as pd
import argparse

from rich import print as rprint

from collections import defaultdict


statistics = defaultdict(lambda: defaultdict(int))


def collect_stats_from_file(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)

            if 'category' in data:
                statistics['category'][data['category']] += 1
            if 'provider' in data:
                statistics['provider'][data['provider']] += 1
            if 'model' in data:
                statistics['model'][data['model']] += 1

            for tag in data.get('tags', []):
                statistics['tags'][tag] += 1

        except yaml.YAMLError as err:
            rprint(f'[bold red][x][/bold red] error getting stats from {file_path}: {err}')


def process_directory(dir_path):
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                collect_stats_from_file(os.path.join(root, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect statistics from prompt-serve files')
    
    parser.add_argument(
        '-d', '--directory',
        help='prompt directory',
        required=True
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        rprint(f'[bold red][x][/bold red] {args.directory} is not a valid directory')
        sys.exit(1)
    
    process_directory(args.directory)

    # cnvert dictionary to dataframe
    df = pd.DataFrame.from_dict({(i,j): statistics[i][j] 
                            for i in statistics.keys() 
                            for j in statistics[i].keys()},
                            orient='index', columns=['Count'])

    dfs = {field: pd.DataFrame(list(values.items()), columns=[field, 'Count']).sort_values('Count', ascending=False) 
        for field, values in statistics.items()}

    # Print our statistics in separate tables
    for field, df in dfs.items():
        rprint(f'[bold]{field}[/bold]')
        if field == 'tags':
            print('(top 5)')
            print(df.head(5).to_string(index=False))  # Only display top 5 for tags
        else:
            print(df.to_string(index=False))
        print('\n')