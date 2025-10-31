import re

from analysis_config import AnalysisConfig
from analysis_exception import AnalysisException
from check_factory import CheckFactory
from checks.check import Check
from models.changed_file import ChangedFile
from models.changed_line import ChangedLine
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class FileAnalyzer:
    def __init__(self, analysis_config: AnalysisConfig, repository_directory: str) -> None:
        self.analysis_config = analysis_config
        self.check_factory: CheckFactory = CheckFactory(analysis_config)
        self.repository_directory = repository_directory
        self.hunk_pattern = r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@'
    
    def analyze_changed_file(self, changed_file: ChangedFile) -> FileAnalysisResult:
        self.__check_file_exclusion(changed_file)
        if self.__is_file_ignored(changed_file):
            return FileAnalysisResult(changed_file.get_relative_path(self.repository_directory))
        file_encoding = self.__get_encoding_for_file(changed_file)
        loaded_file = self.__try_load_changed_file(changed_file, file_encoding)
        return self.__analyze_loaded_file(loaded_file)
    
    def __check_file_exclusion(self, changed_file: ChangedFile):
        if self.__is_file_forbidden_in_diff(changed_file):
            raise AnalysisException(f"The file does not belong into a git repository! Please add it to the .gitignore "
                                    f"or upload it to a proper file sharing service instead!")
    
    def __is_file_forbidden_in_diff(self, changed_file: ChangedFile) -> bool:
        for file_pattern in self.analysis_config.forbidden_files:
            if changed_file.matches_git_pattern(file_pattern):
                return True
        return False
    
    def __is_file_ignored(self, changed_file: ChangedFile) -> bool:
        for file_pattern in self.analysis_config.ignored_files:
            if changed_file.matches_git_pattern(file_pattern):
                return True
        return False
    
    def __get_encoding_for_file(self, changed_file: ChangedFile) -> str:
        for file_pattern, encoding in self.analysis_config.file_encodings.items():
            if changed_file.matches_git_pattern(file_pattern):
                return encoding
        return "utf-8"
    
    def __try_load_changed_file(self, changed_file: ChangedFile, file_encoding: str) -> LoadedFile:
        try:
            return self.__load_changed_file(changed_file, file_encoding)
        except UnicodeDecodeError:
            raise AnalysisException(f"The file is not saved with the correct encoding. The expected encoding is "
                                    f"'{file_encoding}'.")
    
    def __load_changed_file(self, changed_file: ChangedFile, file_encoding: str) -> LoadedFile:
        all_lines = self.__read_changed_file(changed_file.file_path, file_encoding)
        if changed_file.check_entire_file and changed_file.diff is None:
            changed_lines = [ChangedLine(i, line) for i, line in enumerate(all_lines)]
        else:
            numbers_of_added_lines = self.__get_numbers_of_changed_lines(changed_file.diff)
            changed_lines = self.__filter_changed_lines(all_lines, numbers_of_added_lines)
        return LoadedFile(changed_file, file_encoding, all_lines, changed_lines)
    
    def __read_changed_file(self, file_path: str, file_encoding: str) -> list[str]:
        with open(file_path, "r", encoding=file_encoding, errors="replace") as fp:
            return fp.readlines()
        
    def __get_numbers_of_changed_lines(self, diff_text: str | None) -> list[int]:
        if diff_text is None:
            return []
        if diff_text.startswith("Binary files") and diff_text.endswith("differ\n"):
            raise AnalysisException(f"Could not determine diff of binary file. Output from git: '{diff_text}'")
        if not diff_text.startswith("@@") and diff_text.startswith("Binary files") and diff_text.endswith("differ\n"):
            raise UnicodeDecodeError("utf-8", diff_text.encode("utf-8"), 0, 2, 
                                     "Could not properly decode output of 'git diff-tree'. The decoded string does "
                                     "not start with '@@'.")
        return self.__parse_diff_to_changed_line_numbers(diff_text)
    
    def __parse_diff_to_changed_line_numbers(self, diff_text: str) -> list[int]:
        lines = diff_text.split('\n')
        changed_lines = []
        current_line_num = None
        for line in lines:
            current_line_num = self.__process_next_line(current_line_num, line, changed_lines)
        return changed_lines
    
    def __process_next_line(self, current_line_number: int, next_line: str, changed_lines: list[int]) -> int | None:
        hunk_match = re.match(self.hunk_pattern, next_line)
        if hunk_match:
            # reset line number when new hunk was found
            return int(hunk_match.group(3))
        elif current_line_number is not None:
            if next_line.startswith('+') and not next_line.startswith('+++'):
                # Added line
                changed_lines.append(current_line_number)
                return current_line_number + 1
            elif next_line.startswith('-') and not next_line.startswith('---'):
                # Deleted line (don't increment line number)
                return current_line_number
            elif next_line.startswith(' '):
                # Context line (unchanged)
                return current_line_number + 1
        return None
            
    def __filter_changed_lines(self, lines: list[str], numbers_of_added_lines: list[int]) -> list[ChangedLine]:
        return [ChangedLine(i, line) for i, line in enumerate(lines) if i in numbers_of_added_lines]
    
    def __analyze_loaded_file(self, loaded_file: LoadedFile) -> FileAnalysisResult:
        checks = self.__load_checks_for_file(loaded_file)
        return self.__perform_checks_on_loaded_file(loaded_file, checks)

    def __perform_checks_on_loaded_file(self, loaded_file: LoadedFile, checks: list[Check]) -> FileAnalysisResult:
        result = FileAnalysisResult(loaded_file.get_relative_path(self.repository_directory))
        for check in checks:
            issues = check.execute_on_changed_file(loaded_file)
            result.issues += self.__compress_issues(issues)
        return result
    
    def __compress_issues(self, issues: list[LineAnalysisIssue]) -> list[LineAnalysisIssue]:
        if len(issues) <= 3:
            return issues
        else:
            return [LineAnalysisIssue(issues[0].line_number, 
                                      f"The following issue was found multiple times between line "
                                      f"{issues[0].line_number} and {issues[-1].line_number}: "
                                      f"{issues[0].issue_description}")]
            
    def __load_checks_for_file(self, loaded_file: LoadedFile) -> list[Check]:
        checks = self.check_factory.generate_checks(self.analysis_config.standard_checks)
        for wildcard, check_definitions in self.analysis_config.specific_checks.items():
            if loaded_file.matches_git_pattern(wildcard):
                checks += self.check_factory.generate_checks(check_definitions)
        return checks