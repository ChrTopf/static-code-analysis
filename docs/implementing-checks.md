# Implementing New Checks

This guide explains how to create new analysis checks for the Static Code Analysis tool.

## Overview

Checks are the core components that analyze code for specific issues. Each check implements the `Check` interface and operates on changed lines in files.

## Check Interface

All checks must inherit from the abstract `Check` class:

```python
from abc import abstractmethod, ABC
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class Check(ABC):
    @abstractmethod
    def parse_config(self, config_object: dict[str, object] | None):
        pass

    @abstractmethod
    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        pass
```

## Step-by-Step Implementation

### 1. Create the Check Class

Create a new file in the `src/checks/` directory:

```python
# src/checks/my_new_check.py
from checks.check import Check
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class MyNewCheck(Check):
    def __init__(self):
        # Initialize your check
        self.settings = {}

    def parse_config(self, config_object: dict[str, object] | None):
        # Parse and store configuration settings
        self.settings = config_object or {}

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        # Implementation goes here
        return []
```

### 2. Implement the Analysis Logic

The `execute_on_changed_file` method receives:

- `changed_file`: Contains file information and changed lines

And returns a list of `LineAnalysisIssue` objects.

```python
def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
    issues = []
    for line in changed_file.changed_lines:
        # Analyze each changed line
        if self._violates_rule(line.content):
            issue = LineAnalysisIssue(
                line.number,
                f"Issue found: {self._get_issue_description(line.content)}"
            )
            issues.append(issue)
    return issues

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
    def __init__(self):
        self.max_length = 80  # Default value
        self.severity = 'warning'  # Default value

    def parse_config(self, config_object: dict[str, object] | None):
        if config_object:
            # Extract configuration with defaults
            self.max_length = config_object.get('max_length', 80)
            self.severity = config_object.get('severity', 'warning')

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        issues = []
        for line in changed_file.changed_lines:
            if len(line.content) > self.max_length:
                issues.append(LineAnalysisIssue(
                    line.number,
                    f"Line exceeds {self.max_length} characters"
                ))
        return issues
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
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class NoPrintStatements(Check):
    def __init__(self):
        # Match print() calls but not in comments
        self.print_pattern = re.compile(r'^\s*print\s*\(')

    def parse_config(self, config_object: dict[str, object] | None):
        # This check doesn't need configuration
        pass

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        issues = []
        faulty_lines = [
            line for line in changed_file.changed_lines
            if self.print_pattern.search(line.content)
        ]

        for line in faulty_lines:
            issues.append(LineAnalysisIssue(
                line.number,
                "Remove print() statements before committing. Use logging instead."
            ))

        return issues
```

### Example 2: Configurable Check

```python
# src/checks/function_complexity.py
import re
from checks.check import Check
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class FunctionComplexity(Check):
    def __init__(self):
        self.max_complexity = 10  # Default value
        self.function_pattern = re.compile(r'^\s*def\s+(\w+)\s*\(')

    def parse_config(self, config_object: dict[str, object] | None):
        if config_object:
            self.max_complexity = config_object.get('max_complexity', 10)

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        issues = []
        current_function = None
        complexity = 0

        for line in changed_file.changed_lines:
            # Check if this is a function definition
            func_match = self.function_pattern.search(line.content)
            if func_match:
                if current_function and complexity > self.max_complexity:
                    issues.append(LineAnalysisIssue(
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

        return issues
```

### Example 3: Multi-line Analysis

```python
# src/checks/import_organization.py
from checks.check import Check
from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile

class ImportOrganization(Check):
    def __init__(self):
        pass

    def parse_config(self, config_object: dict[str, object] | None):
        # This check doesn't need configuration
        pass

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        issues = []
        import_lines = []

        # Collect all import lines
        for line in changed_file.changed_lines:
            if line.content.strip().startswith(('import ', 'from ')):
                import_lines.append(line)

        if len(import_lines) < 2:
            return issues

        # Check if imports are sorted
        import_texts = [line.content.strip() for line in import_lines]
        sorted_imports = sorted(import_texts)

        if import_texts != sorted_imports:
            issues.append(LineAnalysisIssue(
                import_lines[0].number,
                "Imports should be sorted alphabetically"
            ))

        return issues
```

## Best Practices

### Error Handling

```python
def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
    issues = []
    try:
        # Your analysis logic
        pass
    except Exception as e:
        # Log error but don't fail the entire analysis
        issues.append(LineAnalysisIssue(
            1,
            f"Check failed: {str(e)}"
        ))
    return issues
```

### Performance Considerations

```python
class EfficientCheck(Check):
    def __init__(self):
        # Pre-compile regex patterns
        self.pattern = re.compile(r'your_pattern')
        # Cache expensive computations
        self._cache = {}

    def parse_config(self, config_object: dict[str, object] | None):
        # Handle configuration if needed
        pass

    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        issues = []
        # Process lines efficiently
        relevant_lines = [
            line for line in changed_file.changed_lines
            if self._quick_filter(line.content)
        ]

        for line in relevant_lines:
            # More expensive analysis only on filtered lines
            if self._detailed_check(line.content):
                issues.append(LineAnalysisIssue(line.number, "Issue found"))

        return issues
```

### Configuration Validation

```python
def __init__(self):
    self.max_length = 80  # Default value

def parse_config(self, config_object: dict[str, object] | None):
    if config_object:
        # Validate configuration
        max_length = config_object.get('max_length', 80)
        if not isinstance(max_length, int) or max_length < 1:
            raise ValueError("max_length must be a positive integer")

        self.max_length = max_length
```

## Testing Your Check

See [Testing](getting-started.md#Testing) section in `Getting Started Guide`

## Common Patterns

### File Extension Specific Logic

```python
def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
    issues = []
    file_extension = changed_file.file_path.split('.')[-1].lower()

    if file_extension == 'py':
        issues.extend(self._check_python_specific(changed_file))
    elif file_extension == 'js':
        issues.extend(self._check_javascript_specific(changed_file))

    return issues
```

### Line Context Analysis

```python
def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
    issues = []
    for i, line in enumerate(changed_file.changed_lines):
        # Get surrounding context
        prev_line = changed_file.changed_lines[i-1] if i > 0 else None
        next_line = changed_file.changed_lines[i+1] if i < len(changed_file.changed_lines)-1 else None

        if self._check_with_context(line, prev_line, next_line):
            issues.append(LineAnalysisIssue(line.number, "Context issue"))

    return issues
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