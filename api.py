
import os
import sys
import uuid
import yaml

from flask import Flask, request

from flask_restful import Resource, Api

from uuid import uuid4

from pykwalify.core import Core as ymlvalidator

from server import gitmgr
from server import utils


app = Flask(__name__)
api = Api(app)

config = utils.Config('ps.conf')


class Upload(Resource):
    def post(self):
        data = request.get_json()
        fuuid = uuid.uuid4()
        file_name = f'{fuuid}.yaml'
        file_path = os.path.join(git_repo_path, file_name)

        # this should also parse the file and sort them into categories by that field

        # validate against the schema
        c = ymlvalidator(source_data=data, schema_files=['../schema.yml'])
        c.validate()

        # Save yaml file
        with open(file_path, 'w') as file:
            yaml.dump(data, file)

        repo.add_file(file_path)

        return {'status': 'success', 'message': f'{file_name} uploaded successfully.'}


class Retrieve(Resource):
    def get(self, fuuid):
        file_path = os.path.join(git_repo_path, f'{fuuid}.yaml')

        if not os.path.exists(file_path):
            return {'status': 'failure', 'message': 'File not found.'}, 404

        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        return data


api.add_resource(Upload, '/upload')
api.add_resource(Retrieve, '/retrieve/<string:uuid>')


if __name__ == '__main__':
    global repo
    global git_repo_path

    repo_path = config.get('main', 'repo_path')
    repo_name = config.get('main', 'repo_name')

    repo = gitmgr.Mgr(repo_path, repo_name)
    repo.create_or_use_repo()

    app.run(debug=True)
