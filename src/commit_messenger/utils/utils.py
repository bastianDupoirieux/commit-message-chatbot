from git import Repo
import os

class GitUtils:

    def __init__(self, repo: Repo):
        self.repo = repo

    def get_git_diff(self):

        return self.repo.index.diff("HEAD")

    def see_added_files(self):
        """
        Check the staged files in git
        :return: the added files in git
        """
        git_diff = self.get_git_diff()  # create the diff compared to HEAD
        return [d.a_path for d in git_diff]

    def get_diff_from_staged_files(self, file):
        git_diff = self.get_git_diff()
        diff_index = self.see_added_files().index(file)
        return git_diff[diff_index].diff

    def commit_added_files(self, commit_message):
        commit = self.repo.index.commit(commit_message)
        print(f'Successfuly commited with message: {commit_message} and hash {commit.hexsha}')

class Config:
    def __init__(self, config:dict):
        self.config = config
        self.config_keys = ["commit_mode", "files_to_ignore"] # the required fields
        #Is there a better way to write these required fields outside the class defintion, without a config for the config?

    def run_config_checks(self):
        """Check if the config passed is correct"""
        keys_passed = self.config.keys()
        for key in self.config_keys:
            if key not in keys_passed:
                raise KeyError(f"Missing key value {key} in config")

    def create_error_if_file_should_be_ignored(self, file:os.path):
        if file in self.config["files_to_ignore"]:
            raise ValueError(f"File {file} should be ignored, commit message can't be generated")

class ProjectHandler:
    def __init__(self):
        self.dir = os.getcwd()
        folders_to_ignore = ['.git', '.venv', 'venv', 'env', '.idea'] #certain directories are just technical and should be ignored anyway



    def find_occurence_of_file_in_dir(self, file) -> list:
        pass