import re

from checks.check import Check
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class CSharpMethodLength(Check):
    def __init__(self):
        self.max_lines = 50  # Default value
        # Regex to match C# method/constructor declarations
        self.method_head_pattern = re.compile(
            r'(?:public|private|protected|internal|static|\w+\s+)*' # access modifiers
            r'(?:'
            r'(?:\w+(?:\[\])?(?:<[^>]+>)?\s+\w+\s*\([^)]*\)\s*(?:\{|$))|' # method: returnType methodName(params)
            r'(?:\w+\s*\([^)]*\)\s*(?::\s*\w+\([^)]*\))?\s*)' # constructor: ClassName(params) : base(params)
            r')')

    def parse_config(self, config_object: dict[str, object] | None):
        if config_object:
            max_lines = config_object.get('max_lines', 50)
            if not isinstance(max_lines, int) or max_lines < 1:
                raise ValueError("max_lines must be a positive integer")
            self.max_lines = max_lines

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        # Only process C# files
        if not changed_file.file_path.lower().endswith('.cs'):
            return []

        issues = []

        # If checking entire file, analyze all lines; otherwise only changed lines
        if changed_file.check_entire_file:
            lines_to_check = [(i + 1, line) for i, line in enumerate(changed_file.all_lines)]
        else:
            lines_to_check = [(line.number, line.content) for line in changed_file.changed_lines]

        # Track method/constructor boundaries
        method_start = None
        method_name = None
        brace_count = 0
        method_line_count = 0

        for line_num, line_content in lines_to_check:
            # Check if this line starts a method or constructor
            method_match = self.__contains_method_head(line_content)
            if method_match and method_start is None:
                method_start = line_num
                method_name = self._extract_method_name(line_content)
                method_line_count = 1

                # Check if opening brace is on the same line
                if '{' in line_content:
                    brace_count = 1
                continue

            # If we're inside a method/constructor
            if method_start is not None:
                method_line_count += 1

                # Count braces to track method boundaries
                if '{' in line_content:
                    brace_count += line_content.count('{')
                if '}' in line_content:
                    brace_count -= line_content.count('}')

                    # Method/constructor ends when braces are balanced
                    if brace_count <= 0:
                        if method_line_count > self.max_lines:
                            issues.append(LineAnalysisIssue(
                                method_start,
                                f"Method/constructor '{method_name}' is {method_line_count} lines long, "
                                f"maximum allowed is {self.max_lines} lines"
                            ))

                        # Reset for next method
                        method_start = None
                        method_name = None
                        brace_count = 0
                        method_line_count = 0

        return issues

    def __contains_method_head(self, line: str) -> bool:
        return self.method_head_pattern.search(line) is not None

    def __extract_methods_with_line_numbers(self, cs_file_content: list[str]) -> list[dict]:
        """Extract all method names with their start and end line numbers from C# file content.

        Args:
            cs_file_content: List of strings representing lines of a C# file

        Returns:
            List of dictionaries with keys: 'name', 'start_line', 'end_line'
        """
        methods = []
        method_start = None
        method_name = None
        brace_count = 0

        for line_num, line_content in enumerate(cs_file_content, 1):
            # Check if this line starts a method or constructor
            method_match = self.method_head_pattern.search(line_content)
            if method_match and method_start is None:
                method_start = line_num
                method_name = self._extract_method_name(line_content)

                # Check if opening brace is on the same line
                if '{' in line_content:
                    brace_count = 1
                else:
                    brace_count = 0
                continue

            # If we're inside a method/constructor
            if method_start is not None:
                # Count braces to track method boundaries
                if '{' in line_content:
                    brace_count += line_content.count('{')
                if '}' in line_content:
                    brace_count -= line_content.count('}')

                    # Method/constructor ends when braces are balanced
                    if brace_count <= 0:
                        methods.append({
                            'name': method_name,
                            'start_line': method_start,
                            'end_line': line_num
                        })

                        # Reset for next method
                        method_start = None
                        method_name = None
                        brace_count = 0

        return methods

    def __get_lines_as_string(self, loaded_file: LoadedFile) -> str:
        return "\n".join(loaded_file.all_lines)

    def _extract_method_name(self, line_content: str) -> str:
        """Extract method or constructor name from the declaration line."""
        # Try to extract method name (word before parentheses)
        match = re.search(r'(\w+)\s*\([^)]*\)', line_content)
        if match:
            return match.group(1)

        # Fallback: return a generic identifier
        return "method/constructor"