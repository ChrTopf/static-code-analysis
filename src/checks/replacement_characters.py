from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class ReplacementCharacters(Check):
    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        lines_with_replacement = [line for line in changed_file.changed_lines if line.content.__contains__("�")]
        for line_with_replacement in lines_with_replacement:
            result.issues.append(LineAnalysisIssue(
                line_with_replacement.number,
                f"Replacement character (�) found."
            ))