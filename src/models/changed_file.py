import pathlib

from pathspec import PathSpec


class ChangedFile:
    def __init__(self, file_path: str, diff: bytes | str | None, check_entire_file: bool):
        self.file_path = file_path
        self.diff: bytes | str | None = diff
        self.check_entire_file = check_entire_file

    def get_file_extension(self) -> str:
        return pathlib.Path(self.file_path).suffix
    
    def matches_git_pattern(self, pattern: str) -> bool:
        return PathSpec.from_lines('gitwildmatch', [pattern.strip()]).match_file(self.file_path)
    
    def get_relative_path(self, repository_directory: str) -> str:
        return self.file_path.replace(repository_directory, "")