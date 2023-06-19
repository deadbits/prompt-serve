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
    

    def bare_repo(self):
        msg(f'Initializing bare repo: {self.full_path}')

        try:
            self.repo = Repo.init(self.full_path, bare=True, mkdir=True)
            return True
        except Exception as err:
            msg(f'Failed to initialize repo: {self.full_path} - {err}', 'error')
            return False


    def init_repo(self):
        msg(f'Using existing repo: {self.full_path}')

        try:
            msg(f'Initializing bare repo: {self.full_path}')
            self.repo = Repo(self.full_path)
            return True
        except Exception as err:
            msg(f'Failed to initialize repo: {self.full_path} - {err}', 'error')
            return False


    def create_or_use_repo(self):
        if os.path.exists(self.full_path):
            return self.init_repo()
        else:
            return self.bare_repo()


    def add_file(self, file_path):
        try:
            msg(f'Adding {file_path} to {self.repo_name}')
            self.repo.git.add(file_path)
            msg(f'Commiting {file_path} tp {self.repo_name}')
            self.repo.git.commit('-m', f'Add {file_path}')
            msg(f'Pushing commit to {self.repo_name}')
            self.repo.git.push()
        except Exception as err:
            msg(f'Error adding file: {err}', 'error')
            return False

        return True


    def get_file_list(self):
        self.repo.git.pull()
        return self.repo.git.ls_files()
