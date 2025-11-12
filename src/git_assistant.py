import os

from git import DiffIndex, Diff, Repo, InvalidGitRepositoryError, Remote

from models.changed_file import ChangedFile


class GitAssistant:
    def __init__(self, repo_directory: str):
        self.repo: Repo | None = None
        if not self.__try_set_git_repository(repo_directory):
            found_repo_directory = self.__find_git_directory()
            self.__try_set_git_repository(found_repo_directory)
        
    def reset_repository_directory(self, repo_directory: str):
        self.repo = Repo(repo_directory)
    
    def get_local_branches(self):
        if self.repo is None:
            return []
        return [head.name for head in self.repo.heads]
    
    def get_remote_branches(self):
        if self.repo is None:
            return []
        return [remote.name for remote in self.repo.remotes.origin.refs]
    
    def get_repository_directory(self) -> str:
        return self.repo.working_dir

    def get_changes_of_pull_request(self, source_branch: str, target_branch: str, changed_lines_only: bool) \
            -> list[ChangedFile]:
        if self.repo is None:
            return []
        self.__check_for_uncommitted_changes()
        self.__update_branch(target_branch)
        self.__update_branch(source_branch)
        local_source_branch = self.__get_local_branch_for_remote_branch(source_branch)
        local_target_branch = self.__get_local_branch_for_remote_branch(target_branch)
        diff = self.__get_diff_of_pull_request(local_source_branch, local_target_branch)
        return self.__get_changed_files_from_diff(diff, changed_lines_only)
        
    def __check_for_uncommitted_changes(self):
        if self.repo.is_dirty():
            if self.repo.untracked_files:
                raise Exception("Untracked files detected: {repo.untracked_files} Please commit your changes first!")
            if self.repo.index.diff("HEAD"):
                raise Exception("Staged changes detected. Please commit your changes first!")
            if self.repo.index.diff(None):
                raise Exception("Unstaged changes detected. Please commit your changes first!")
            raise Exception("Uncommitted changes detected. Please commit your changes first!")
        
    def __update_branch(self, branch_name: str):
        if branch_name.startswith("origin/"):
            local_branch_name = self.__get_local_branch_for_remote_branch(branch_name)
            if not self.__local_branch_exists(local_branch_name):
                self.__checkout_remote_branch(branch_name, local_branch_name)
            else:
                self.repo.git.checkout(local_branch_name)
        else:
            self.repo.git.checkout(branch_name)
        self.__pull_current_branch()

    def __get_local_branch_for_remote_branch(self, branch_name: str) -> str:
        return branch_name.replace("origin/", "")
        
    def __local_branch_exists(self, branch_name: str) -> bool:
        return branch_name in [branch.name for branch in self.repo.branches]

    def __checkout_remote_branch(self, remote_branch_name: str, local_branch_name: str):
        # Create new local branch tracking the remote branch
        head = self.repo.create_head(local_branch_name, remote_branch_name)
        head.checkout()
        
    def __pull_current_branch(self):
        origin: Remote = self.repo.remotes.origin
        current_branch = self.repo.active_branch.name
        origin.pull(current_branch)
        
    def __get_commit_of_merge_base(self, source_branch: str, target_branch: str):
        merge_base = self.repo.merge_base(source_branch, target_branch)
        return merge_base[0] if merge_base else None
    
    def __get_diff_of_pull_request(self, source_branch: str, target_branch: str):
        commit = self.__get_commit_of_merge_base(source_branch, target_branch)
        source_branch_head = self.repo.heads[source_branch].commit
        return commit.diff(source_branch_head, create_patch=True, textconv=True)
        
    def __get_changed_files_from_diff(self, diff: DiffIndex[Diff], changed_lines_only: bool) -> list[ChangedFile]:
        changes = []
        for changed_file_info in diff:
            if not changed_file_info.deleted_file:
                changes.append(self.__parse_diff_to_changed_file(changed_file_info, changed_lines_only))
        return changes

    def __parse_diff_to_changed_file(self, diff_metadata: Diff, changed_lines_only: bool) -> ChangedFile:
        file_path = self.repo.working_dir + os.path.sep + diff_metadata.b_path
        check_entire_file = (not changed_lines_only and not diff_metadata.renamed_file) or diff_metadata.new_file
        diff = self.__decode_diff(diff_metadata.diff)
        return ChangedFile(file_path, diff, check_entire_file)
    
    def __decode_diff(self, diff: bytes | None) -> str | None:
        if diff is None:
            return None
        else:
            return diff.decode(encoding="utf-8", errors="strict")

    def __try_set_git_repository(self, repo_directory: str) -> bool:
        try:
            self.repo = Repo(repo_directory)
            return True
        except InvalidGitRepositoryError:
            return False

    def __find_git_directory(self):
        start_path = os.getcwd()
        current_path = os.path.abspath(start_path)
        while True:
            git_path = os.path.join(current_path, '.git')
            if os.path.isdir(git_path):
                return current_path  # Return the repository root, not the .git directory
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:  # Reached root directory
                return None
            current_path = parent_path

