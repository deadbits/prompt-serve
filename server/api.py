import os
import sys
import yaml
import aiofiles
import configparser
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from git import Repo
from uuid import UUID
from typing import Optional
from starlette.responses import FileResponse
from fastapi.params import Path


app = FastAPI()


class Config:
    def __init__(self, config_file):
        # check if config file exists
        self.config_file = config_file
        if not os.path.exists(self.config_file):
            print(f'config file not found: {self.config_file}', 'error')
            sys.exit(1)

        # load config file
        print(f'loading config file: {self.config_file}', 'status')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get(self, section, key):
        # get config option by section and key name
        answer = None

        try:
            answer = self.config.get(section, key)
        except:
            print(f'config file missing option: {section} {key}', 'error')

        return answer


config = Config('../ps.conf')
global REPO_HOME
REPO_HOME = config.get('main', 'repo_path')


def verify_dir_is_repo(repo_path: str) -> bool:
    try:
        repo = Repo(repo_path)
        return True
    except:
        return False


def parse_yaml(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data


@app.post('/{repo_name}')
async def upload_file(repo_name: str, file: UploadFile = File(...)):
    try:
        repo_path = os.path.join(REPO_HOME, repo_name)
        if not verify_dir_is_repo(repo_path):
            raise HTTPException(status_code=400, detail=f'directory is not a git repository: {repo_path}')

        file_path = os.path.join(repo_path, file.filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        repo = Repo(repo_path)
        repo.git.add([file_path])
        repo.index.commit('Add file through API')
        msg = {'filename': file.filename, 'message': 'file uploaded and committed successfully'}
        
        return msg
    
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))


@app.get('/{repo_name}/_name/{prompt_name}', responses={200: {'content': {'application/x-yaml': {}}}})
async def read_file_by_name(repo_name: str, prompt_name: str, raw: Optional[bool] = Query(None)):
    repo_path = os.path.join(REPO_HOME, repo_name)
    if not verify_dir_is_repo(repo_path):
        raise HTTPException(status_code=400, detail=f'directory is not a git repository: {repo_path}')

    file_path = os.path.join(repo_path, f'{prompt_name}.yml')
    
    if os.path.exists(file_path):
        data = parse_yaml(file_path)
        
        if raw:
            return {'prompt': data.get('prompt')}
        else:
            return FileResponse(file_path, media_type='application/x-yaml')
    
    else:
        raise HTTPException(status_code=404, detail=f'File not found: {file_path}')


@app.get('/{repo_name}/_uuid/{prompt_uuid}', responses={200: {'content': {'application/x-yaml': {}}}})
async def read_file_by_uuid(repo_name: str, prompt_uuid: UUID, raw: Optional[bool] = Query(None)):
    repo_path = os.path.join(REPO_HOME, repo_name)
    if not verify_dir_is_repo(repo_path):
        raise HTTPException(status_code=400, detail=f'directory is not a git repository: {repo_path}')

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.yml'):
                file_location = os.path.join(root, file)
                data = parse_yaml(file_location)
                
                if data.get('uuid') == str(prompt_uuid):
                    if raw:
                        return {'prompt': data.get('prompt')}
                    else:
                        return FileResponse(file_location, media_type='application/x-yaml')
    
    raise HTTPException(status_code=404, detail=f'File not found for UUID: {prompt_uuid}')