# https://github.com/deadbits/prompt-serve
# example of converting a prompt-serve template to a langchain PromptTemplate object
import os
import sys
import yaml
import json
import argparse

from rich import print as rprint

from langchain import PromptTemplate


def convert(path_to_ps_prompt):
    rprint(f'[bold white][~][/bold white] converting template {path_to_ps_prompt}')
    
    with open(path_to_ps_prompt, 'r') as fp:
        try:
            data = yaml.safe_load(fp)
            prompt = data['prompt']
            
            # check if prompt-serve template contains input variables
            if 'input_vars' in data.keys():
                input_vars = data['input_vars']
                langchain_template = PromptTemplate(template=prompt, input_variables=input_vars)
            
            # otherwise we only use the prompt
            else:
                langchain_template = PromptTemplate(template=prompt)
     
            return (data, langchain_template)
     
        except Exception as err:
            print(f'[x] caught exception: {err}')
            return (None, None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert prompt-serve template to langchain PromptTemplate')

    parser.add_argument(
        '-f', '--file', 
        help='prompt-serve template to convert', 
        required=True
    )

    args = parser.parse_args()
     
    if not os.path.exists(args.file):
        rprint(f'[bold red][x][/bold red] template {args.file} not found')
        sys.exit(1)
    
    original, langchain_template = convert(args.file)
    if original is None or langchain_template is None:
        rprint(f'[bold red][x][/bold red] failed to convert template {args.file}')
        sys.exit(1)
    
    rprint(f'[bold green][+][/bold green] successfully converted template {args.file}')
    rprint(f'[bold blue]prompt-serve[/bold blue]:')
    print(json.dumps(original, indent=2))
    print('\n')
    print('--' * 50)
    print('\n')
    rprint(f'[bold orange3]langchain[/bold orange3]:')
    print(json.dumps(langchain_template.dict(), indent=2))