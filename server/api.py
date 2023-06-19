
import os
import sys
import uuid
import yaml

from flask import Flask, request, jsonify, send_file

from uuid import uuid4

from pykwalify.core import Core as ymlvalidator

from werkzeug.utils import secure_filename

from lib import gitmgr
from lib.utils import msg
from lib.utils import Config


app = Flask(__name__)
config = Config('ps.conf')


@app.route('/upload', methods=['POST'])
def upload():
    msg('uploading new prompt', 'status')

    if 'file' not in request.files:
        msg('no file part', 'error')
        return jsonify(error='no file'), 400
    
    file = request.files['file']

    if file.filename == '':
        msg('no selected file', 'error')
        return jsonify(error='no filename'), 400
    
    if file:        
        fuuid = str(uuid.uuid4())
        filename = f'{fuuid}.yaml'

        try:
            msg(f'trying to load yaml: {filename}')
            data = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            return jsonify(error=str(exc)), 400
        
        # validate against the schema
        msg('validating yaml against schema')
        c = ymlvalidator(source_data=data, schema_files=['../schema.yml'])
        c.validate()

        file_path = os.path.join(full_path, f'{fuuid}.yaml')
        msg(f'writing new prompt to file: {file_path}')
        with open(file_path, 'w') as file:
            yaml.dump(data, file)

        repo.add_file(file_path)

        return jsonify(message='prompt successfully uploaded and committed'), 200


@app.route('/retrieve/<uuid>', methods=['GET'])
def retrieve(uuid):
    # Assuming files are saved with their uuid as the filename
    filename = secure_filename(uuid + '.yaml')
    file_path = os.path.join(full_path, filename)
    msg(f'retrieving file: {file_path}')

    if os.path.exists(file_path):
        try:
            msg(f'returning file: {file_path}')
            return send_file(file_path, mimetype='application/x-yaml')
        except Exception as err:
            msg(f'error returning file: {err}', 'error')
            return jsonify(error=str(err)), 500
    else:
        msg(f'file not found: {file_path}', 'error')
        return jsonify(error='File not found'), 404



if __name__ == '__main__':
    global repo
    global full_path

    repo_path = config.get('main', 'repo_path')
    repo_name = config.get('main', 'repo_name')
    full_path = os.path.join(repo_path, repo_name)

    repo = gitmgr.Mgr(repo_path, repo_name)

    app.run(debug=True)
