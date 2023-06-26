#!/usr/bin/env python3
# create.py
# github.com/deadbits/prompt-serve
# interactively create a prompt in prompt-serve yaml format

import sys
import os
import yaml
import uuid
import argparse

from rich import print
from rich.prompt import Prompt


def ask_for_input(field_name, field_type, is_required, default_value=None):
    value = None
    
    if is_required:
        while not value:
            value = Prompt.ask(f'[bold]{field_name} ({field_type})[/bold]')
    else:
        value = Prompt.ask(f'[bold]{field_name} ({field_type}) [optional, default={default_value}][/bold]') or default_value

    if value:
        if field_type == 'int':
            value = int(value)
        elif field_type == 'float':
            value = float(value)
        elif field_type == 'bool':
            value = value.lower() in ['true', 't', 'false', 'f']
        elif field_type == 'seq':
            value = [item.strip() for item in value.split(',')]
    return value


def create_map():
    # create the YAML map
    map_info = {}

    map_info['title'] = ask_for_input('title', 'str', True)
    map_info['uuid'] = str(uuid.uuid4())
    map_info['description'] = ask_for_input('description', 'str', True)
    map_info['category'] = ask_for_input('category', 'str', True)
    map_info['provider'] = ask_for_input('provider', 'str', False)
    map_info['model'] = ask_for_input('model', 'str', False)
    
    # model settings with default values
    model_settings_fields = ['temperature', 'top_k', 'top_p', 'max_tokens', 'stream', 'presence_penalty', 'frequency_penalty']
    model_settings_types = ['float', 'int', 'float', 'int', 'bool', 'float', 'float']
    model_settings_defaults = [0.8, None, 1, None, False, 0.0, 0.0]
    
    model_settings = {field: ask_for_input(field, ftype, False, default) for field, ftype, default in zip(model_settings_fields, model_settings_types, model_settings_defaults)}
    
    # only add model_settings to map if it's not empty
    if any(model_settings.values()):
        map_info['model_settings'] = model_settings

    map_info['prompt'] = ask_for_input('prompt', 'str', True)
    
    # Sequence fields
    seq_fields = ['references', 'associations', 'packs', 'tags']
    for field in seq_fields:
        map_info[field] = ask_for_input(field, 'seq', False)

    return map_info



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate YAML files against the prompt-serve schema.')
    
    parser.add_argument(
        '-n', '--name',
        help='prompt file name to create',
        required=True
    )

    args = parser.parse_args()

    print(f'[bold]creating prompt file {args.name} ...[/bold]')

    if os.path.exists(args.name):
        print(f'[bold][red](error)[/red][/bold] file {args.name} already exists')
        sys.exit(1)
    
    map_info = create_map()
    
    try:
        with open(args.name, 'w') as outfile:
            yaml.dump(map_info, outfile, sort_keys=False)
        
        if os.path.exists(args.name):
            print(f'[bold] successfully wrote file {args.name}[/bold]')

    except Exception as err:
        print(f'[bold][red](error)[/red][/bold] failed to write file {args.name}: {str(err)}')
        print(yaml.safe_dump(map_info, sort_keys=False))