import re

from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class TODO(Check):
    def __init__(self):
        super()
        self.regex = r"todo([^u]|\s)"

    def parse_config(self, config_object: dict[str, object] | None):
        pass

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        faulty_lines = [
            line for line in changed_file.changed_lines 
            if len(re.findall(self.regex, line.content, re.IGNORECASE)) > 0
        ]
        for faulty_line in faulty_lines:
            result.issues.append(LineAnalysisIssue(
                faulty_line.number,
                "Found unresolved TODO. Please use user stories instead!"
            ))
        