from git import Repo


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
        print(f'Successfuly commited with message: {commit_message} with hash {commit.hexsha}')


#Define a function just to get the added files

#Define a function to get the git diff from all staged files

#Define a function to commit the files from the staging area using a commit message
