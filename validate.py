import os
import sys
import uuid
import argparse

import yaml
from pykwalify.core import Core


# store uuids in a set to check for uniqueness
seen_uuids = set()


def validate_file(file_path):
    # load the yaml file
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    # check for uniqueness of uuid
    uuid = data.get('uuid')
    if uuid in seen_uuids:
        raise ValueError(f'[error] UUID {uuid} in file {file_path} is not unique.')
    seen_uuids.add(uuid)

    # validate against the schema
    c = Core(source_data=data, schema_files=[SCHEMA_PATH])
    # will raise an exception if validation fails
    c.validate()


def validate_directory(directory_path, create=False):
    # walk the directory and validate each file
    for root, dirs, files in os.walk(directory_path):

        for file in files:
            # only validate yaml files
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)

                # validate the file
                try:
                    validate_file(file_path)
                    print(f'[+] {file_path} is valid.')
                except Exception as e:
                    print(f'[x] validation failed for {file_path}\n{str(e)}')
                    if create:
                        new_uuid = str(uuid.uuid4())
                        print(f'[+] new uuid: {new_uuid}')
                
                print('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate YAML files against the prompt-serve schema.')
    
    parser.add_argument(
        '-s', '--schema',
        help='schema file to validate against',
        required=False,
        default='schema.yml'
    )

    parser.add_argument(
        '-f', '--file', 
        help='single file to validate', 
        required=False
    )

    parser.add_argument(
        '-d', '--directory',
        help='directory to validate',
        required=False
    )

    parser.add_argument(
        '-c', '--create',
        help='create new uuids if validation fails',
        required=False,
        action='store_true'
    )

    args = parser.parse_args()

    if not os.path.exists(args.schema):
        print(f'[error] chema file {args.schema} does not exist.')
        sys.exit(1)

    SCHEMA_PATH = args.schema
    CREATE = args.create

    if args.file:
        validate_file(args.file)
    elif args.directory:
        validate_directory(args.directory, CREATE)
    else:
        parser.print_help()
        sys.exit(1)