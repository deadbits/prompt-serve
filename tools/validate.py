#!/usr/bin/env python
# validate.py
# github.com/deadbits/prompt-serve
# validate prompt-serve yaml files against the schema
import os
import sys
import uuid
import argparse
import yaml
import pandas as pd

from rich import print as rprint
from collections import defaultdict
from pykwalify.core import Core


# store uuids in a set to check for uniqueness
seen_uuids = set()
statistics = defaultdict(lambda: defaultdict(int))
passed = 0
failed = 0


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
            rprint(f'[bold red](error)[/bold red] error getting stats from {file_path}: {err}')


def validate_file(file_path, create=False):
    global passed, failed
    # load the yaml file
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    # check for uniqueness of uuid
    f_uuid = data.get('uuid')

    if f_uuid in seen_uuids:
        rprint(f'[bold red](error)[/bold red] UUID {f_uuid} in file {file_path} is not unique.')

        # create a new uuid if requested
        if create:
            new_uuid = str(uuid.uuid4())
            rprint(f'[bold blue](new uuid)[/bold blue] {new_uuid}')
    
    seen_uuids.add(f_uuid)

    # validate against the schema
    c = Core(source_data=data, schema_files=[SCHEMA_PATH])

    try:
        c.validate()
        rprint(f'[bold green](status)[/bold green] {file_path} is valid.')
        passed += 1
    except Exception as e:
        rprint(f'[bold red](error)[/bold red] {file_path} is invalid: {str(e)}')
        failed += 1


def validate_directory(directory_path, create=False, stats=False):
    # walk the directory and validate each file
    for root, dirs, files in os.walk(directory_path):

        for file in files:
            # only validate yaml files
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                validate_file(file_path, create)
                
                if stats:
                    collect_stats_from_file(file_path)


def display_stats():
    # convert dictionary to dataframe
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
            print(df.head(5).to_string(index=False))
        else:
            print(df.to_string(index=False))
        print('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate YAML prompts against the prompt-serve schema.')
    
    parser.add_argument(
        '-s', '--schema',
        help='schema file to validate against',
        required=False,
        default='schema.yml'
    )

    parser.add_argument(
        '-f', '--file', 
        help='single prompt to validate', 
        required=False
    )

    parser.add_argument(
        '-d', '--directory',
        help='directory of prompts to validate',
        required=False
    )

    parser.add_argument(
        '-c', '--create',
        help='create new uuids if validation fails',
        required=False,
        action='store_true'
    )

    parser.add_argument(
        '-g', '--gen-stats',
        help='generate statistics from directory',
        required=False,
        default=False,
        action='store_true'
    )

    args = parser.parse_args()

    if not os.path.exists(args.schema):
        rprint(f'[bold red](error)[/bold red] schema file {args.schema} does not exist.')
        sys.exit(1)

    SCHEMA_PATH = args.schema
    CREATE = args.create
    STATS = args.gen_stats

    if args.file:
        validate_file(args.file)
    elif args.directory:
        validate_directory(args.directory, CREATE, STATS)
        if STATS:
            print('\n')
            display_stats()
        rprint(f'\n[bold]Passed:[/bold] {passed} prompts')
        rprint(f'[bold red]Failed:[/bold red] {failed} prompts')
    else:
        parser.print_help()
        sys.exit(1)