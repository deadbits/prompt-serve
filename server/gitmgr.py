import os

from git import Repo
from git import InvalidGitRepositoryError

from .utils import msg


class Mgr:
    def __init__(self, repo_path, repo_name):
        self.repo_name = repo_name
        self.repo_path = repo_path
        self.full_path = os.path.join(self.repo_path, self.repo_name)
        self.repo = None
        
        if not os.path.exists(self.full_path):
            msg(f'creating new repo: {self.full_path}')
            self.repo = Repo.init(self.full_path, mkdirs=True)
        else:
            try:
                msg(f'loading existing repo: {self.full_path}')
                self.repo = Repo(self.full_path)
            except Exception as err:
                msg(f'error loading repo: {err}', 'error')
                

    def add_file(self, file_path):
        try:
            msg(f'Adding {file_path} to {self.repo_name}')
            self.repo.index.add([file_path])
            msg(f'Commiting {file_path} tp {self.repo_name}')
            self.repo.index.commit(f'Add {file_path}')
            #msg(f'Pushing commit to {self.repo_name}')
            #self.repo.git.push()
        except Exception as err:
            msg(f'Error adding file: {err}', 'error')
            return False

        return True


    def get_file_list(self):
        self.repo.git.pull()
        return self.repo.git.ls_files()
