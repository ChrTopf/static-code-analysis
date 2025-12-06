# Getting Started - Developer Guide

This guide helps developers set up and work with the Static Code Analysis tool codebase.

## Prerequisites

- Python 3.10 or higher
- PyQt5 for GUI components
- json5 library for configuration parsing
- Git (for repository operations)

## Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd static-code-analysis
```

### 2. Install Dependencies

```bash
chmod +x setup-venv.sh
./setup-venv.sh
```

### 3. Project Structure

```
src/
├── main.py                     # Application entry point
├── analysis.py                 # Core analysis engine
├── analysis_config.py          # Configuration data model
├── config_parser.py            # Configuration file parser
├── cli_argument_parser.py      # Command line argument handling
├── headless_analyzer.py        # Headless mode implementation
├── file_analyzer.py            # File analysis logic
├── git_assistant.py            # Git operations
├── logger.py                   # Logging functionality
├── check_factory.py            # Check instantiation factory
├── analysis_exception.py       # Custom exceptions
├── models/                     # Data models
│   ├── analysis_arguments.py
│   ├── cli_arguments.py
│   ├── changed_file.py
│   ├── changed_line.py
│   ├── file_analysis_result.py
│   ├── line_analysis_issue.py
│   ├── loaded_file.py
│   └── repository_info.py
├── checks/                     # Analysis checks
│   ├── check.py               # Base check interface
│   ├── line_length.py
│   ├── tabs.py
│   ├── todo.py
│   ├── trailing_whitespace.py
│   ├── replacement_characters.py
│   └── region_newline.py
├── gui/                        # GUI components (MVC pattern)
│   ├── main_view.py           # Main GUI view
│   ├── main_model.py          # GUI data model
│   ├── main_controller.py     # GUI controller
│   ├── themeable.py           # Theme support
│   ├── adapter/               # GUI adapters
│   ├── commands/              # Command pattern implementation
│   └── view/                  # GUI view components
└── util/                       # Utility functions
    └── analysis_result_formatter.py
```

## Running the Application

### GUI Mode (Default)

```bash
python src/main.py
```

### Headless Mode

```bash
python src/main.py --headless --repository /path/to/repo --source feature-branch --target main
```

### Command Line Options

- `--headless`: Run without GUI
- `--repository`: Repository path (headless mode)
- `--source`: Source branch name (headless mode)
- `--target`: Target branch name (headless mode)
- `--changed-lines-only`: Analyze only changed lines
- `--quiet`: Suppress output
- `--config`: Path to configuration file

## Architecture Overview

The application follows a clean architecture with separation of concerns:

### MVC Pattern (GUI)

- **Model** (`main_model.py`): Manages application state and data
- **View** (`main_view.py`): Handles UI components and user interactions
- **Controller** (`main_controller.py`): Coordinates between model and view

### Core Components

#### Analysis Engine

- `analysis.py`: Orchestrates the analysis process
- `file_analyzer.py`: Analyzes individual files
- `git_assistant.py`: Handles Git operations (diff, branch operations)

#### Check System

- `check.py`: Abstract base class for all checks
- Individual check implementations in `checks/` directory
- `check_factory.py`: Creates check instances based on configuration

#### Configuration System

- `config_parser.py`: Parses JSON5 configuration files
- `analysis_config.py`: Configuration data model
- Supports both standard and file-specific checks

### Data Flow

1. **Initialization**: Load configuration and parse command line arguments
2. **Git Analysis**: Determine changed files between branches (with support for remote branch checkout)
3. **File Loading**: Load and parse changed files with proper encoding
4. **Check Execution**: Run configured checks on changed lines (with improved error handling and encoding support)
5. **Result Compilation**: Aggregate results and format output

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Keep classes focused on single responsibilities
- Use descriptive variable and function names

### Adding New Features

1. **New Checks**: Extend the `Check` base class
2. **GUI Components**: Follow MVC pattern and use command pattern for actions
3. **Configuration**: Update `config_parser.py` for new configuration options
4. **Models**: Add data classes in `models/` directory for new data structures

### Testing

The codebase features unit tests for checks. The source code for tests must be placed in the `test` directory and sample files which are used for testing the checks must be placed in `samples` directory. 

The following code snippet shows an example of a unit test:

```python
import unittest

from checks.csharp_method_length import CSharpMethodLength
from util.test_butler import TestButler
from util.test_config import TestConfig

class TestStringMethods(unittest.TestCase):

    def test_csharp_method_length(self):
        sample_file = "samples/CoffeeShop.cs"
        expected_result = [48]
        check_config = {"max_lines": 20}
        check = CSharpMethodLength()

        butler = TestButler(self)
        butler.execute_test(TestConfig(sample_file, expected_result, check_config, check))

if __name__ == '__main__':
    unittest.main()
```

The test case is called `test_csharp_method_length` and uses the `TestButler` to execute on a sample file called `CoffeeShop.cs`. The expected result is a list of line numbers or a list of `LineAnalysisIssue` instances. The check config must be a dictionary and it must contain the same information which usually gets parsed from `analysis_config.json5`. Lastly, the check is instanciated by calling its constructor and tested by creating a `TestButler` and telling it to run the test with the specified config.

### Error Handling

- Use custom exceptions from `analysis_exception.py`
- Provide meaningful error messages to users
- Log errors using the `logger.py` module

## Common Development Tasks

### Adding a New Check

1. Create a new class inheriting from `Check` in the `checks/` directory
2. Implement the `execute_on_changed_file` method
3. Update `check_factory.py` to include the new check
4. Add configuration options if needed

### Modifying the GUI

1. Update the view component in `gui/view/`
2. Add new commands in `gui/commands/` if needed
3. Update the controller to handle new interactions
4. Follow the existing command pattern for user actions

### Adding CLI Options

1. Update `cli_argument_parser.py` to add new arguments
2. Modify `models/cli_arguments.py` if new data model fields are needed
3. Update the main application logic to handle new options

## Debugging

### Logging

The application includes comprehensive logging:

```python
from logger import Logger
logger = Logger(quiet=False)
logger.debug("Debug message")
```

### GUI Debugging

- Use Qt debugging tools for GUI issues
- Check the console output for PyQt5 warnings and errors

### Git Operations

- Test Git operations manually using `git_assistant.py`
- Verify branch existence and repository state

## Build and Distribution

### Creating Executable

The project includes build scripts for creating standalone executables:

```bash
# Run the build script
chmod +x build.sh
./build.sh
```

### Configuration for End Users

- Ensure `analysis_config.json5` is included in the distribution
- Provide default configuration that works for common scenarios
- Document any additional setup requirements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes following the coding guidelines
4. Test thoroughly (manual testing until automated tests are available)
5. Submit a pull request with a clear description of changes

## Troubleshooting

### Common Issues

**PyQt5 Installation Issues**

```bash
# On Linux
sudo apt-get install python3-pyqt5

# On Windows/Mac
pip install PyQt5
```

**Git Repository Not Found**

- Ensure the selected directory is a valid Git repository
- Check that the repository has the specified branches
- Verify read permissions on the repository directory

**Configuration File Errors**

- Validate JSON5 syntax using an online validator
- Check that all required configuration sections are present
- Ensure file paths in configuration use forward slashes

**Encoding Issues**

- Verify file encodings are correctly specified in configuration
- Check that files actually use the specified encoding
- Test with a small subset of files first