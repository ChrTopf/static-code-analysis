# Implementing New Checks

This guide explains how to create new analysis checks for the Static Code Analysis tool.

## Overview

Checks are the core components that analyze code for specific issues. Each check implements the `Check` interface and operates on changed lines in files.

## Check Interface

All checks must inherit from the abstract `Check` class:

```python
from abc import abstractmethod, ABC
from models.file_analysis_result import FileAnalysisResult
from models.loaded_file import LoadedFile

class Check(ABC):
    @abstractmethod
    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        pass
```

## Step-by-Step Implementation

### 1. Create the Check Class

Create a new file in the `src/checks/` directory:

```python
# src/checks/my_new_check.py
from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class MyNewCheck(Check):
    def __init__(self, settings=None):
        # Initialize your check with optional settings
        self.settings = settings or {}

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        # Implementation goes here
        pass
```

### 2. Implement the Analysis Logic

The `execute_on_changed_file` method receives:

- `changed_file`: Contains file information and changed lines
- `result`: Object to store analysis issues

```python
def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
    for line in changed_file.changed_lines:
        # Analyze each changed line
        if self._violates_rule(line.content):
            issue = LineAnalysisIssue(
                line.number,
                f"Issue found: {self._get_issue_description(line.content)}"
            )
            result.issues.append(issue)

def _violates_rule(self, line_content: str) -> bool:
    # Your rule logic here
    return False

def _get_issue_description(self, line_content: str) -> str:
    # Return descriptive error message
    return "Describe the issue"
```

### 3. Handle Configuration

Support configuration parameters for flexibility:

```python
class ConfigurableCheck(Check):
    def __init__(self, settings=None):
        self.settings = settings or {}
        # Extract configuration with defaults
        self.max_length = self.settings.get('max_length', 80)
        self.severity = self.settings.get('severity', 'warning')

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        for line in changed_file.changed_lines:
            if len(line.content) > self.max_length:
                result.issues.append(LineAnalysisIssue(
                    line.number,
                    f"Line exceeds {self.max_length} characters"
                ))
```

### 4. Register the Check

Add your check to the `CheckFactory`:

```python
# src/check_factory.py
from checks.my_new_check import MyNewCheck

class CheckFactory:
    def __init__(self, analysis_config: AnalysisConfig):
        self.analysis_config = analysis_config
        self.all_checks: dict[str, type] = {
            "line_length": LineLength,
            "my_new_check": MyNewCheck,  # Add your check here
            # ... other checks
        }
```

### 5. Update Configuration

Add your check to the configuration schema:

```json5
// analysis_config.json5
{
  "standard_checks": {
    "my_new_check": null  // For checks without parameters
  },
  "specific_checks": {
    "*.py": {
      "my_new_check": {    // For checks with parameters
        "max_length": 88,
        "severity": "error"
      }
    }
  }
}
```

## Complete Examples

### Example 1: Simple Pattern Check

```python
# src/checks/no_print_statements.py
import re
from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class NoPrintStatements(Check):
    def __init__(self, settings=None):
        self.settings = settings or {}
        # Match print() calls but not in comments
        self.print_pattern = re.compile(r'^\s*print\s*\(')

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        faulty_lines = [
            line for line in changed_file.changed_lines
            if self.print_pattern.search(line.content)
        ]

        for line in faulty_lines:
            result.issues.append(LineAnalysisIssue(
                line.number,
                "Remove print() statements before committing. Use logging instead."
            ))
```

### Example 2: Configurable Check

```python
# src/checks/function_complexity.py
import re
from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class FunctionComplexity(Check):
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.max_complexity = self.settings.get('max_complexity', 10)
        self.function_pattern = re.compile(r'^\s*def\s+(\w+)\s*\(')

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        current_function = None
        complexity = 0

        for line in changed_file.changed_lines:
            # Check if this is a function definition
            func_match = self.function_pattern.search(line.content)
            if func_match:
                if current_function and complexity > self.max_complexity:
                    result.issues.append(LineAnalysisIssue(
                        line.number - 1,  # Previous function
                        f"Function '{current_function}' has complexity {complexity}, "
                        f"maximum allowed is {self.max_complexity}"
                    ))
                current_function = func_match.group(1)
                complexity = 1
            elif current_function:
                # Count complexity indicators
                if any(keyword in line.content for keyword in ['if', 'elif', 'for', 'while', 'except']):
                    complexity += 1
```

### Example 3: Multi-line Analysis

```python
# src/checks/import_organization.py
from checks.check import Check
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class ImportOrganization(Check):
    def __init__(self, settings=None):
        self.settings = settings or {}

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        import_lines = []

        # Collect all import lines
        for line in changed_file.changed_lines:
            if line.content.strip().startswith(('import ', 'from ')):
                import_lines.append(line)

        if len(import_lines) < 2:
            return

        # Check if imports are sorted
        import_texts = [line.content.strip() for line in import_lines]
        sorted_imports = sorted(import_texts)

        if import_texts != sorted_imports:
            result.issues.append(LineAnalysisIssue(
                import_lines[0].number,
                "Imports should be sorted alphabetically"
            ))
```

## Best Practices

### Error Handling

```python
def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
    try:
        # Your analysis logic
        pass
    except Exception as e:
        # Log error but don't fail the entire analysis
        result.issues.append(LineAnalysisIssue(
            1,
            f"Check failed: {str(e)}"
        ))
```

### Performance Considerations

```python
class EfficientCheck(Check):
    def __init__(self, settings=None):
        # Pre-compile regex patterns
        self.pattern = re.compile(r'your_pattern')
        # Cache expensive computations
        self._cache = {}

    def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
        # Process lines efficiently
        relevant_lines = [
            line for line in changed_file.changed_lines
            if self._quick_filter(line.content)
        ]

        for line in relevant_lines:
            # More expensive analysis only on filtered lines
            if self._detailed_check(line.content):
                result.issues.append(LineAnalysisIssue(line.number, "Issue found"))
```

### Configuration Validation

```python
def __init__(self, settings=None):
    self.settings = settings or {}

    # Validate configuration
    max_length = self.settings.get('max_length', 80)
    if not isinstance(max_length, int) or max_length < 1:
        raise ValueError("max_length must be a positive integer")

    self.max_length = max_length
```

## Testing Your Check

### Manual Testing

1. Create a test repository with sample files
2. Add your check to the configuration
3. Run the analysis and verify results

### Integration Testing

```python
# Test script example
from checks.my_new_check import MyNewCheck
from models.changed_line import ChangedLine
from models.loaded_file import LoadedFile
from models.file_analysis_result import FileAnalysisResult

def test_my_check():
    check = MyNewCheck({'max_length': 50})

    # Create test data
    test_lines = [
        ChangedLine(1, "short line"),
        ChangedLine(2, "this is a very long line that exceeds the limit")
    ]
    test_file = LoadedFile("test.py", test_lines, [])
    result = FileAnalysisResult("test.py")

    # Run check
    check.execute_on_changed_file(test_file, result)

    # Verify results
    assert len(result.issues) == 1
    assert result.issues[0].line_number == 2

if __name__ == "__main__":
    test_my_check()
    print("Check test passed!")
```

## Common Patterns

### File Extension Specific Logic

```python
def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
    file_extension = changed_file.file_path.split('.')[-1].lower()

    if file_extension == 'py':
        self._check_python_specific(changed_file, result)
    elif file_extension == 'js':
        self._check_javascript_specific(changed_file, result)
```

### Line Context Analysis

```python
def execute_on_changed_file(self, changed_file: LoadedFile, result: FileAnalysisResult):
    for i, line in enumerate(changed_file.changed_lines):
        # Get surrounding context
        prev_line = changed_file.changed_lines[i-1] if i > 0 else None
        next_line = changed_file.changed_lines[i+1] if i < len(changed_file.changed_lines)-1 else None

        if self._check_with_context(line, prev_line, next_line):
            result.issues.append(LineAnalysisIssue(line.number, "Context issue"))
```

## Troubleshooting

### Common Issues

**Check Not Found**

- Ensure the check is registered in `CheckFactory`
- Verify the class name matches the factory registration

**Configuration Not Working**

- Check the JSON5 syntax in the configuration file
- Verify parameter names match what your check expects

**Performance Issues**

- Pre-compile regex patterns in `__init__`
- Use efficient filtering to reduce expensive operations
- Consider line-by-line vs. full-file analysis trade-offs

**Import Errors**

- Ensure all required imports are included
- Check the module path structure

Remember to test your checks thoroughly with various input scenarios and edge cases to ensure reliable operation.