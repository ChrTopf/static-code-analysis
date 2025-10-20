from checks.check import Check
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class TrailingWhitespace(Check):
    def __init__(self):
        self.max_trailing_whitespaces = None

    def parse_config(self, config_object: dict[str, object]):
        self.max_trailing_whitespaces = config_object["max_trailing_whitespaces"]

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        issues = []
        faulty_lines = [
            line for line in changed_file.changed_lines
            if (len(line.content) - len(line.content.rstrip())) > self.max_trailing_whitespaces
        ]
        for faulty_line in faulty_lines:
            issues.append(LineAnalysisIssue(
                faulty_line.number,
                f"Line {faulty_line.number} includes more than {self.max_trailing_whitespaces} trailing whitespaces."
            ))
        return issues