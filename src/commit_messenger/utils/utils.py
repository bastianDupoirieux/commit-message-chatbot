from git import Repo
import os
from collections import defaultdict

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
        project_handler = ProjectHandler()
        self.project_files = project_handler.files_in_dir

    def run_config_checks(self):
        """Check if the config passed is correct"""
        # Check if the required keys are present in the config
        keys_passed = self.config.keys()
        for key in self.config_keys:
            if key not in keys_passed:
                raise KeyError(f"Missing key value {key} in config")

        if type(self.config["files_to_ignore"]) != list:
            type_given = self.config["files_to_ignore"]
            raise TypeError(f"files_to_ignore must be a list, given type {type_given}")

        #Check if the file that should be ignored in the config is unique in the working dir
        for f in self.config["files_to_ignore"]:
            if len(self.project_files[f]) > 1:
                raise ValueError(f"File {f} exists multiple times in the working directory"
                                 f"as files {', '.join(self.project_files[f])}, please specify"
                                 f"which files should be ignored in the config")

    def create_error_if_file_should_be_ignored(self, file:os.path):
        """
        Raise an error if a file should be ignored. Handles files differently depending on whether
        the absolute path of the file has been given
        :param file:
        :return:
        """

        if os.path.isfile(file):
            pass # Do I need any handling depending on whether it is a path or just a basename?
        if file in self.config["files_to_ignore"]:
            raise ValueError(f"File {file} should be ignored, commit message can't be generated")

class ProjectHandler:
    def __init__(self):
        self.dir = os.getcwd()
        directories_to_ignore = [os.path.join(self.dir, '.git'),
                                 os.path.join(self.dir, '.venv'),
                                 os.path.join(self.dir, 'venv'),
                                 os.path.join(self.dir, 'env'),
                                 os.path.join(self.dir, '.idea')] #certain directories are just technical and should be ignored anyway
        all_files = defaultdict(list) #a dictionary containing the paths to all different files
        # This loop doesn't work properly, when running in the top directory __init__.py should have at least two occurences
        for root, dirs, files in os.walk(self.dir):
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in directories_to_ignore]

            for f in files:
                filepath = os.path.join(root, f)
                if os.path.isfile(filepath):
                    all_files[f].append(filepath)

        self.files_in_dir = all_files
