from checks.check import Check
from models.line_analysis_issue import LineAnalysisIssue


class TestConfig:
    def __init__(self,
                 sample_file_path: str,
                 expected_result: list[LineAnalysisIssue] | list[int] | None,
                 config_object: dict[str, object] | None,
                 check: Check) -> None:
        self.sample_file_path: str = sample_file_path
        self.expected_result: list[LineAnalysisIssue] | list[int] | None = expected_result
        self.config_object: dict[str, object] | None = config_object
        self.check: Check = check
        