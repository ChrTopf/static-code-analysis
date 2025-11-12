from unittest import TestCase

from models.changed_file import ChangedFile
from models.changed_line import ChangedLine
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class TestButler:
    
    def __init__(self, test_case: TestCase) -> None:
        self.test_case: TestCase = test_case

    def generate_new_file_diff(self, file_path: str, file_encoding: str = "UTF-8") -> LoadedFile:
        return self.generate_file_diff(file_path, numbers_of_changed_lines=None, file_encoding=file_encoding)
    
    def generate_file_diff(self, file_path: str, 
                           numbers_of_changed_lines: list[int] | None, 
                           file_encoding: str = "UTF-8") -> LoadedFile:
        all_lines = self.__read_file(file_path, file_encoding)
        changed_file = ChangedFile(file_path, None, False)
        changed_lines = [ChangedLine(i, line) for i, line in enumerate(all_lines, 1) 
                         if numbers_of_changed_lines is None or i in numbers_of_changed_lines]
        return LoadedFile(changed_file, file_encoding, all_lines, changed_lines)
    
    def __read_file(self, file_path: str, file_encoding: str) -> list[str]:
        with open(file_path, "r", encoding=file_encoding, errors="strict") as fp:
            return fp.readlines()
        
    def verify_check_results(self, 
                             target_results: list[LineAnalysisIssue] | list[int] | None, 
                             actual_results: list[LineAnalysisIssue]) -> None:
        self.test_case.assertIsNotNone(actual_results, "The list of results must not be None type.")
        if target_results is None:
            self.test_case.assertTrue(len(actual_results) == 0,
                                       "The target issues are empty, but the actual issues are not.")
        else:
            self.__verify_equal_issue_length(target_results, actual_results)
            self.__verify_equal_issues(target_results, actual_results)
                
    def __verify_equal_issue_length(self, 
                                    target_results: list[LineAnalysisIssue] | list[int],
                                    actual_results: list[LineAnalysisIssue]) -> None:
        error_message = self.__generate_error_message(
            "The amount of found issues is not equal to the amount of expected issues.",
            target_results,
            actual_results)
        self.test_case.assertEqual(len(target_results), len(actual_results), error_message)
        
    def __verify_equal_issues(self,
                              target_results: list[LineAnalysisIssue] | list[int],
                              actual_results: list[LineAnalysisIssue]) -> None:
        for result in target_results:
            if result is LineAnalysisIssue:
                line_number = result.line_number
            else:
                line_number = result
            found_issue = self.__find_issue(line_number, target_results, actual_results)
            if result is LineAnalysisIssue:
                pass
            
    def __find_issue(self, wanted_line: int,
                     target_results: list[LineAnalysisIssue] | list[int],
                     actual_results: list[LineAnalysisIssue]) -> LineAnalysisIssue:
        found_issue_line_numbers = [issue.line_number for issue in actual_results]
        error_message = self.__generate_error_message(
            f"An issue was expected to be found for line {wanted_line}, but no issue was present.",
            target_results,
            actual_results)
        self.test_case.assertIn(wanted_line, found_issue_line_numbers, error_message)
        return [issue for issue in actual_results if issue.line_number == wanted_line][0]
    
    def __verify_issue_text(self, 
                            target_issue: LineAnalysisIssue, 
                            actual_issue: LineAnalysisIssue, 
                            target_results: list[LineAnalysisIssue], 
                            actual_results: list[LineAnalysisIssue]) -> None:
        error_message = self.__generate_error_message(
            f"The issue description for the issue in line {target_issue.line_number} does not match the "
            f"expected description.\n"
            f"The expected description was '{target_issue.issue_description}'.\n"
            f"The actual description was '{actual_issue.issue_description}'.'", 
            target_results, 
            actual_results)
        self.test_case.assertEqual(target_issue.issue_description, actual_issue.issue_description, error_message)
        
    def __generate_error_message(self, message: str,
                                 target_results: list[LineAnalysisIssue] | list[int], 
                                 actual_results: list[LineAnalysisIssue]):
        return (message + "\nExpected issues:\n" + self.__prettify_issues(target_results) + 
                "\nActual issues:\n" + self.__prettify_issues(actual_results))
    
    def __prettify_issues(self, issues: list[LineAnalysisIssue] | list[int]) -> str:
        return "\n".join([
            "- " + str(issue.line_number) + ": " + issue.issue_description 
            if issue is LineAnalysisIssue else "- " + str(issue) for issue in issues
        ])
        