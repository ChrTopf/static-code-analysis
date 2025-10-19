from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class Tabs(Check):
    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        faulty_lines = [line for line in changed_file.changed_lines if line.content.__contains__("\t")]
        for faulty_line in faulty_lines:
            result.issues.append(LineAnalysisIssue(
                faulty_line.number,
                f"Found tab character. Please use space character instead!"
            ))