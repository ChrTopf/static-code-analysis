# Analysis Configuration Guide

This document explains how to configure the static code analysis tool using the `analysis_config.json5` file.

## Configuration File Location

The configuration file should be placed in the root directory of your project as `analysis_config.json5`. The application will automatically load this file when performing analysis.

## Configuration Structure

The configuration file uses JSON5 format (JSON with comments and trailing commas support) and contains the following main sections:

### Forbidden Files

Specify files that should not be present in the repository:

```json5
{
  "forbidden_files": [
    "*.doc",
    "*.exe",
    "*.dll",
    "*.msi"
  ]
}
```

- Uses GitHub-flavored wildcards
- Prevents certain file types from being committed
- Common examples: Office documents, executables, compiled libraries

### Ignored Files

Files that should be excluded from static code analysis:

```json5
{
  "ignored_files": [
    "*.md",
    "**/*.gitignore",
    "*.exe",
    "*.mp3",
    "*.gif"
  ]
}
```

- Uses GitHub-flavored wildcards
- These files won't be analyzed for code quality issues
- Typical exclusions: documentation, binary files, configuration files

### File Encodings

Specify the expected encoding for different file types:

```json5
{
  "file_encodings": {
    "*.sql": "utf-16le",
    "*.cs": "utf-16le",
    "*.py": "utf-8",
    "*.js": "utf-8",
    "*.html": "utf-8"
  }
}
```

- UTF-8 is the default encoding if not specified
- SQL and C# files often use UTF-16LE
- Python, JavaScript, and web files typically use UTF-8

### Standard Checks

Checks applied to all analyzed files:

```json5
{
  "standard_checks": {
    "tabs": null,
    "todo": null,
    "replacement_characters": null
  }
}
```

Available standard checks:

- **tabs**: Detects tab characters in code
- **todo**: Finds TODO comments in code
- **replacement_characters**: Detects � characters (encoding issues)

### Specific Checks

File-type-specific checks with configurable parameters:

```json5
{
  "specific_checks": {
    "*.sql": {
      "line_length": null,
      "trailing_whitespace": {"max_trailing_whitespaces": 20}
    },
    "*.cs": {
      "line_length": {"max_line_length": 120},
      "trailing_whitespace": {"max_trailing_whitespaces": 20}
    }
  }
}
```

Available specific checks:

- **line_length**: Maximum line length (configurable with `max_line_length`)
- **trailing_whitespace**: Maximum trailing spaces (configurable with `max_trailing_whitespaces`)
- **region_newline**: Ensures proper spacing around C# regions

## Available Checks Reference

| Check                  | Type     | Description             | Configuration                      |
| ---------------------- | -------- | ----------------------- | ---------------------------------- |
| tabs                   | Standard | Detects tab characters  | `null`                             |
| todo                   | Standard | Finds TODO comments     | `null`                             |
| replacement_characters | Standard | Detects � characters    | `null`                             |
| line_length            | Specific | Maximum line length     | `{"max_line_length": 120}`         |
| trailing_whitespace    | Specific | Maximum trailing spaces | `{"max_trailing_whitespaces": 20}` |
| region_newline         | Specific | C# region formatting    | `null`                             |

## Example Configuration

Here's a complete example configuration:

```json5
{
  "forbidden_files": [
    "*.exe",
    "*.dll",
    "*.doc*",
    "*.ppt*"
  ],
  "ignored_files": [
    "*.md",
    "**/*.gitignore",
    "*.exe",
    "*.jpg",
    "*.png"
  ],
  "file_encodings": {
    "*.sql": "utf-16le",
    "*.cs": "utf-16le",
    "*.py": "utf-8",
    "*.js": "utf-8"
  },
  "standard_checks": {
    "tabs": null,
    "todo": null,
    "replacement_characters": null
  },
  "specific_checks": {
    "*.py": {
      "line_length": {"max_line_length": 88},
      "trailing_whitespace": {"max_trailing_whitespaces": 0}
    },
    "*.cs": {
      "line_length": {"max_line_length": 120},
      "trailing_whitespace": {"max_trailing_whitespaces": 20},
      "region_newline": null
    },
    "*.sql": {
      "line_length": null,
      "trailing_whitespace": {"max_trailing_whitespaces": 20}
    }
  }
}
```

## Configuration Tips

1. **Start Simple**: Begin with the standard checks enabled and add specific checks as needed
2. **Team Standards**: Align configuration with your team's coding standards
3. **Language-Specific**: Use different rules for different programming languages
4. **Gradual Adoption**: Start with lenient settings and gradually make them stricter
5. **Version Control**: Commit the configuration file to ensure consistency across the team