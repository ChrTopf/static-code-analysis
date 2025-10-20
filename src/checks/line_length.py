from checks.check import Check
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class LineLength(Check):
    def __int__(self):
        self.max_line_length = None

    def parse_config(self, config_object: dict[str, object] | None):
        self.max_line_length = config_object["max_line_length"]

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        issues = []
        faulty_lines = [line for line in changed_file.changed_lines if len(line.content) > self.max_line_length]
        for faulty_line in faulty_lines:
            issues.append(LineAnalysisIssue(
                faulty_line.number,
                f"Line is longer than {self.max_line_length} characters."
            ))
        return issues
