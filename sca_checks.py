import os
import re
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    file_path: str
    line_number: int
    issue_description: str

def check_encoding(directory : str, file_type : str = ".sql", desired_encoding : str = "utf-16le"):
    # search the specified dataset directory for all images
    for root, directories, files in os.walk(directory):
        for file in files:
            if file.endswith(file_type) and "node_modules" not in root:
                for result in check_file(root, file, desired_encoding):
                    print(f"File '{result.file_path}' Line {result.line_number}: {result.issue_description}")

def check_file(parent_directory : str, file_name : str, desired_encoding : str = None, enforcing : bool = True, changed_lines : list[int] = None, config : ConfigManager = None) -> list[AnalysisResult]:
    results = []
    try:
        if config is None:
            config = ConfigManager()
        
        if desired_encoding is None:
            desired_encoding = config.get_file_encoding(file_name)
            
        with open(f"{parent_directory}{os.path.sep}{file_name}", "r", encoding=desired_encoding) as fp:
            lines = fp.readlines()
            
            if config.is_check_enabled("check_unknown_characters"):
                check_unknown_characters(lines, results, file_name, changed_lines)
            if enforcing and config.is_check_enabled("check_line_length"):
                check_config = config.get_check_config("check_line_length")
                max_length = check_config.get("max_length", 120)
                check_line_length(lines, results, file_name, max_length, changed_lines)
            if config.is_check_enabled("check_trailing_spaces"):
                check_config = config.get_check_config("check_trailing_spaces")
                max_trailing = check_config.get("max_trailing_whitespaces", 10)
                check_trailing_spaces(lines, results, file_name, max_trailing, changed_lines)
            if config.is_check_enabled("check_todo"):
                check_todo(lines, results, file_name, changed_lines)
            if config.is_check_enabled("check_region"):
                check_region(lines, results, file_name, changed_lines)
            if config.is_check_enabled("check_tabs"):
                check_tabs(lines, results, file_name, changed_lines)

    except Exception as e:
        results.append(AnalysisResult(
            file_path=file_name,
            line_number=0,
            issue_description=f"Could not perform static code analysis. Error: {e}"
        ))
    return results

def check_unknown_characters(lines : list[str], results : list[AnalysisResult], file_name : str, changed_lines : list[int] = None):
    for i, line in enumerate(lines):
        line_num = i + 1
        if changed_lines is None or line_num in changed_lines:
            if line.__contains__("�"):
                results.append(AnalysisResult(
                    file_path=file_name,
                    line_number=line_num,
                    issue_description=f"Broken character at line {line_num}"
                ))

def check_line_length(lines : list[str], results : list[AnalysisResult], file_name : str, max_line_length : int = 120, changed_lines : list[int] = None):
    too_long_lines = []
    for i, line in enumerate(lines):
        line_num = i + 1
        if changed_lines is None or line_num in changed_lines:
            if len(line.rstrip()) > max_line_length:
                too_long_lines.append(line_num)
    if len(too_long_lines) == 1:
        results.append(AnalysisResult(
            file_path=file_name,
            line_number=too_long_lines[0],
            issue_description=f"Line {too_long_lines[0]} is longer than {max_line_length} characters."
        ))
    elif len(too_long_lines) == 2:
        results.append(AnalysisResult(
            file_path=file_name,
            line_number=too_long_lines[0],
            issue_description=f"Lines {too_long_lines[0]} and {too_long_lines[1]} are longer than {max_line_length} characters."
        ))
    elif len(too_long_lines) > 2:
        results.append(AnalysisResult(
            file_path=file_name,
            line_number=too_long_lines[0],
            issue_description=f"Between line {too_long_lines[0]} and line {too_long_lines[-1]} there are multiple lines which are longer than {max_line_length} characters."
        ))

def check_trailing_spaces(lines : list[str], results : list[AnalysisResult], file_name : str, max_trailing_whitespaces : int = 10, changed_lines : list[int] = None):
    for i, line in enumerate(lines):
        line_num = i + 1
        if changed_lines is None or line_num in changed_lines:
            if (len(line) - len(line.rstrip())) > max_trailing_whitespaces:
                results.append(AnalysisResult(
                    file_path=file_name,
                    line_number=line_num,
                    issue_description=f"Line {line_num} includes more than {max_trailing_whitespaces} trailing whitespaces."
                ))

def check_todo(lines : list[str], results : list[AnalysisResult], file_name : str, changed_lines : list[int] = None):
    regex = r"todo([^u]|\s)"
    for i, line in enumerate(lines):
        line_num = i + 1
        if changed_lines is None or line_num in changed_lines:
            if len(re.findall(regex, line, re.IGNORECASE)) > 0:
                results.append(AnalysisResult(
                    file_path=file_name,
                    line_number=line_num,
                    issue_description=f"Line {line_num} contains an unresolved TODO."
                ))

def check_region(lines : list[str], results : list[AnalysisResult], file_name : str, changed_lines : list[int] = None):
    for i, line in enumerate(lines):
        line_num = i + 1
        if changed_lines is None or line_num in changed_lines:
            if line.__contains__("#region") or line.__contains__("#endregion"):
                if i - 1 >= 0 and len(lines[i - 1].strip()) != 0 and lines[i - 1].strip() != "{":
                    results.append(AnalysisResult(
                        file_path=file_name,
                        line_number=line_num,
                        issue_description=f"Line {line_num} contains a region tag, but is missing an empty line before the region."
                    ))
                if i + 1 <= len(lines) and len(lines[i + 1].strip()) != 0 and lines[i + 1].strip() != "}":
                    results.append(AnalysisResult(
                        file_path=file_name,
                        line_number=line_num,
                        issue_description=f"Line {line_num} contains a region tag, but is missing an empty line after the region."
                    ))

def check_tabs(lines : list[str], results : list[AnalysisResult], file_name : str, changed_lines : list[int] = None):
    for i, line in enumerate(lines):
        line_num = i + 1
        if changed_lines is None or line_num in changed_lines:
            if line.__contains__("\t"):
                results.append(AnalysisResult(
                    file_path=file_name,
                    line_number=line_num,
                    issue_description=f"Line {line_num} contains at least one tab character."
                ))

