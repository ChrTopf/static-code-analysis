from abc import ABC

from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class TrailingWhitespace(Check, ABC):
    def __init__(self, max_trailing_whitespaces: int):
        self.max_trailing_whitespaces = max_trailing_whitespaces

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        faulty_lines = [
            line for line in changed_file.changed_lines
            if (len(line.content) - len(line.content.rstrip())) > self.max_trailing_whitespaces
        ]
        for faulty_line in faulty_lines:
            result.issues.append(LineAnalysisIssue(
                faulty_line.number,
                f"Line {faulty_line.number} includes more than {self.max_trailing_whitespaces} trailing whitespaces."
            ))