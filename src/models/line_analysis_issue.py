from dataclasses import dataclass

@dataclass
class LineAnalysisIssue:
    line_number: int
    issue_description: str