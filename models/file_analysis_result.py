from models.line_analysis_issue import LineAnalysisIssue


class FileAnalysisResult:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.issues: list[LineAnalysisIssue] = []