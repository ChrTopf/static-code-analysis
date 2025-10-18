from checks.check import Check
from models.changed_line import ChangedLine
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class RegionNewline(Check):        
    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        for changed_line in changed_file.changed_lines:
            self.__perform_check_for_line(changed_file, changed_line, result)
                
    def __perform_check_for_line(self, changed_file: LoadedFile, changed_line: ChangedLine, result: FileAnalysisResult):
        if self.__line_contains_region_tag(changed_line.content):
            self.__check_empty_line_before(changed_file, changed_line.number, result)
    
    def __line_contains_region_tag(self, line: str) -> bool:
        if line is None:
            return False
        return line.__contains__("#region") or line.__contains__("#endregion")
    
    def __check_empty_line_before(self, changed_file: LoadedFile, line_number: int, result: FileAnalysisResult):
        line_before = line_number - 1
        if line_before < 0:
            return
        if not self.__is_line_empty(changed_file.all_lines[line_before]):
            result.issues.append(LineAnalysisIssue(line_before, f"Line {line_number} contains a region tag, but is "
                                                                f"missing an empty line before the region."))
            
    def __check_empty_line_after(self, changed_file: LoadedFile, line_number: int, result: FileAnalysisResult):
        line_after = line_number + 1 
        if line_after >= len(changed_file.all_lines):
            return
        if not self.__is_line_empty(changed_file.all_lines[line_after]):
            result.issues.append(LineAnalysisIssue(line_after, f"Line {line_number} contains a region tag, but is "
                                                               f"missing an empty line after the region."))
    
    def __is_line_empty(self, line: str):
        return len(line.strip()) == 0
        