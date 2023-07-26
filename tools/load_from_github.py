#!/usr/bin/env python
# load a prompt-serve template from a github repo
# designed for repostories with a directory structure of:
# /prompts/$category/$promptname.yml

import os
import sys
import json
import yaml
import argparse
import requests


class PromptLoader:    
    def __init__(self):
        self.base_url = 'https://raw.githubusercontent.com'


    def get_template(self, full_repo_name, full_prompt_name) -> str:
        prompt_data = None

        try:
            repo_user, repo_name = full_repo_name.split('/')
        except Exception as err:
            print(f'(error) failed to parse repo name - exception: {err}')
            print('name should be in the format of username/repo')
            return prompt_data
    
        url = f'{self.base_url}/{repo_user}/{repo_name}/main/prompts/{full_prompt_name}.yml'
        full_prompt_name = full_prompt_name + '.yml' if not full_prompt_name.endswith('.yml') else full_prompt_name

        print(f'(status) retrieving template: {url}')
    
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f'(error) error retrieving template - non 200 status code: {response.status_code}')
                return prompt_data
    
            prompt_data = yaml.safe_load(response.text)

        except Exception as err:
            print(f'(error) error retrieving template - exception: {err}')
            return prompt_data

        return prompt_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate YAML prompts against the prompt-serve schema.')
    
    parser.add_argument(
        '-r', '--repo',
        help='repo name (e.g. deadbits/prompt-serve)',
        required=False,
        default='deadbits/prompt-serve'
    )

    parser.add_argument(
        '-p', '--prompt',
        help='prompt as category/name (e.g. instruct/summarize)',
        required=True,
        action='store'
    )

    parser.add_argument(
        '-s', '--save', 
        help='save prompt to file', 
        required=False,
        action='store'
    )

    parser.add_argument(
        '-j', '--json',
        help='output prompt as json (default is yaml)',
        required=False,
        action='store_true'
    )

    args = parser.parse_args()

    loader = PromptLoader()
    prompt_data = loader.get_template(args.repo, args.prompt)

    if prompt_data is None:
        sys.exit(1)

    if args.save:
        if os.path.exists(args.save):
            print(f'(error) file already exists: {args.save}')
            sys.exit(1)
        
        with open(args.save, 'w') as fp:
            yaml.dump(prompt_data, fp)
        
        print(f'(status) prompt saved to file: {args.save}')
    
    elif args.json:
        print(json.dumps(prompt_data, indent=2))
    else:
        print(yaml.dump(prompt_data, indent=2))

