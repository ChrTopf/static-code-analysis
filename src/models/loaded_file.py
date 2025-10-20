from models.changed_file import ChangedFile
from models.changed_line import ChangedLine


class LoadedFile(ChangedFile):
    def __init__(self, 
                 changed_file: ChangedFile, 
                 file_encoding: str, 
                 all_lines: list[str], 
                 changed_lines: list[ChangedLine]):
        super().__init__(changed_file.file_path, changed_file.diff, changed_file.check_entire_file)
        self.file_encoding = file_encoding
        self.all_lines = all_lines
        self.changed_lines = changed_lines