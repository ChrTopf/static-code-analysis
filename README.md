# Static Code Analysis for Pull Requests

A Python-based tool that analyzes changes between Git branches according to Clean Code principles and generates actionable TODO lists for Pull Request reviews. The tool supports both GUI and headless modes, making it suitable for both interactive use and CI/CD integration.

| Property      | Value                                                                             |
| ------------- | --------------------------------------------------------------------------------- |
| Author        | ChrTopf                                                                           |
| Sponsor       | TheHolyException                                                                  |
| Last Modified | 27.10.2025                                                                        |
| Tags          | `Git`<br/>`Pull Request`<br/>`Clean Code`<br/>`Static Code Analysis`<br/>`Python` |

## Preview

![](./assets/20251019%20preview.png)

## Quick Start

### Installation

#### Option 1: Build From Source

This assumes that you already have python 3.8 or higher installed on your system.
Setting up from source also works on windows with batch files instead of the shell scripts.

```bash
git clone https://github.com/ChrTopf/static-code-analysis
cd static-code-analysis
chmod +x setup-venv.sh
chmod +x build.sh
./setup-venv.sh
./build.sh
```

#### Option 2: Executable (Windows)

1. Download the latest release from the GitHub releases page
2. Move the application to your desired location
3. Make sure you have the `analysis_config.json5` file stored in the repository you want to be checked or in the working directory of the executable. 
4. Run `Static Code Analysis.exe`

### Basic Usage

#### GUI Mode

Just run the built tool by double clicking on it. This works for Windows and GNU/Linux.

#### Headless Mode (CI/CD)

```bash
python src/main.py --headless --repository /path/to/repo --source feature-branch --target main
```

Tipp: Use the headless mode paired with git hooks. Learn more about git hooks [here](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

## Documentation

📚 **Comprehensive Documentation Available:**

- **[📋 Configuration Guide](docs/configuration.md)** - Complete guide to `analysis_config.json5` setup and available checks
- **[🚀 Getting Started Guide](docs/getting-started.md)** - Developer setup, architecture overview, and development guidelines
- **[🔧 Implementing New Checks](docs/implementing-checks.md)** - Step-by-step guide for creating custom analysis checks
- **[🔑 SSH Keys Setup](docs/setup-ssh-keys.md)** - Instructions for Git SSH configuration

## Features

- **🖥️ Dual Mode Operation**: GUI for interactive use, headless for CI/CD integration
- **⚙️ Configurable Analysis**: Customizable rules via `analysis_config.json5`
- **📁 Smart File Handling**: Automatic encoding detection and file filtering
- **🔍 Focused Analysis**: Only analyzes changed lines between branches
- **🌟 Clean Code Focus**: Enforces coding standards and best practices
- **🏗️ Extensible Architecture**: Easy to add new checks and rules

## Workflow

1. **Repository Selection**: Choose Git repository root directory
2. **Branch Configuration**: Select source and target branches
3. **Analysis Execution**: Tool processes file differences
4. **Results Review**: View categorized issues and suggested improvements
5. **Integration**: Copy results to Pull Request comments

## Available Checks

| Check                      | Description                       | Configurable    |
| -------------------------- | --------------------------------- | --------------- |
| **Line Length**            | Enforces maximum line length      | ✅ Max length    |
| **Trailing Whitespace**    | Detects excessive trailing spaces | ✅ Max count     |
| **TODO Comments**          | Finds unresolved TODO items       | ❌               |
| **Tab Characters**         | Detects tab usage                 | ❌               |
| **Replacement Characters** | Finds encoding issues (�)         | ❌               |
| **Region Formatting**      | C# region spacing                 | ❌               |
| **File Encodings**         | Validates expected encodings      | ✅ Per file type |

## Use Cases

### Pull Request Quality Assurance

Perfect for ensuring clean code standards before merge:

- Run analysis on feature branches before creating PR
- Generate TODO lists for code review comments
- Enforce team coding standards automatically
- Reduce reviewer workload by catching common issues

### CI/CD Integration

Integrate into your development pipeline:

```bash
# In your CI pipeline
python src/main.py --headless --repository . --source $CI_BRANCH --target main --quiet
```

### Team Development

- Standardize code quality across team members
- Onboard new developers with consistent standards
- Maintain legacy code quality during refactoring

## Architecture

The application follows clean architecture principles with clear separation of concerns:

```
┌─────────────────┬─────────────────┬─────────────────┐
│   Presentation  │    Business     │      Data       │
│     Layer       │     Layer       │     Layer       │
├─────────────────┼─────────────────┼─────────────────┤
│ • GUI (PyQt5)   │ • Analysis      │ • Git           │
│ • CLI Interface │ • Check System  │ • File System   │
│ • Controllers   │ • Configuration │ • Config Files  │
└─────────────────┴─────────────────┴─────────────────┘
```

**Key Components:**

- **MVC Pattern**: Clean separation between UI, logic, and data
- **Plugin Architecture**: Extensible check system
- **Configuration Management**: Flexible JSON5-based settings
- **Git Integration**: Robust branch and diff operations

## Contributing

We welcome contributions! Please see our documentation for guidelines:

1. **Read the Documentation**: Start with the [Getting Started Guide](docs/getting-started.md)
2. **Follow Standards**: Ensure your code follows the existing patterns
3. **Add Tests**: Include tests for new functionality
4. **Update Docs**: Update relevant documentation for changes

### Adding New Checks

See the [Implementing New Checks](docs/implementing-checks.md) guide for detailed instructions.

## Support

- 📖 **Documentation**: Check the `docs/` directory for comprehensive guides
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💡 **Feature Requests**: Submit enhancement ideas via GitHub Issues
- 🔧 **Configuration Help**: See [Configuration Guide](docs/configuration.md)

## License

-> See LICENSE
This project is maintained by ChrTopf and sponsored by TheHolyException.

---

## Version History

| Date/Version | Changes                                                                                                                                                        |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 19.10.2025   | Initial version released                                                                                                                                       |
| 20.10.2025   | - Fixed analysis config parsing issue<br/>- Fixed file encoding issues<br/>- Fixed empty diff issue<br/>- Added automatic checkout feature for remote branches |
| 27.10.2025   | - Added feature for analyzing entire repository by selecting same source and target branch                                                                     |
