from models.line_analysis_issue import LineAnalysisIssue


class FileAnalysisResult:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.issues: list[LineAnalysisIssue] = []
        
    def has_issues(self):
        return len(self.issues) > 0
    
    def get_prettied_issues(self) -> list[str]:
        return [f"Line: {issue.line_number} Issue: {issue.issue_description}" for issue in self.issues]