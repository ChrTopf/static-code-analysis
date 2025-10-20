from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class LineLength(Check):
    def __int__(self):
        self.max_line_length = None

    def parse_config(self, config_object: dict[str, object] | None):
        self.max_line_length = config_object["max_line_length"]

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        too_long_lines = [line for line in changed_file.changed_lines if len(line.content) > self.max_line_length]
        if len(too_long_lines) == 1:
            result.issues.append(LineAnalysisIssue(
                too_long_lines[0].number,
                f"Line {too_long_lines[0]} is longer than {self.max_line_length} characters."
            ))
        elif len(too_long_lines) == 2:
            result.issues.append(LineAnalysisIssue(
                too_long_lines[0].number,
                f"Lines {too_long_lines[0]} and {too_long_lines[1]} are longer than {self.max_line_length} characters."
            ))
        elif len(too_long_lines) > 2:
            result.issues.append(LineAnalysisIssue(
                too_long_lines[0].number,
                f"Between line {too_long_lines[0]} and line {too_long_lines[-1]} there are multiple lines which are "
                f"longer than {self.max_line_length} characters."
            ))
