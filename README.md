# Static Code Analysis for Pull Requests

This program analyzes all changes between branches in a Git repository with regard to Clean Code principles and outputs a TODO list containing all detected anomalies. This list can then be copy-pasted as a comment under a Pull Request in TFS manually.

| Property      | Value                                                                                |
| ------------- | ------------------------------------------------------------------------------------ |
| Author        | ChrTopf                                                                              |
| Sponsor       | TheHolyException                                                                     |
| Last Modified | 25.07.2025                                                                           |
| Tags          | `DevOps`<br/>`Pull Request`<br/>`Clean Code`<br/>`Static Code Analysis`<br/>`Python` |

## Preview



## Getting Started

### Installation

1. Download the latest release from the GitHub releases page of this repository.
2. Optional: For a satisfactory experienc, copy the build output directory into the repository where you want to use the static code analysis.
3. Execute the `Static Code Analysis.exe` by double clicking on it to run the application.
4. Optional: Configure the analysis in `config.json`.

### Usage

1. Execute the `Static Code Analysis.exe` by double clicking on it to run the application.

2. The GUI application will launch with the following workflow:
   
   - **Repository Selection**: Choose the root directory of a Git repository
   - **Source Branch**: Select the branch containing changes for the Pull Request
   - **Target Branch**: Select the target branch where changes will be merged
   - **Perform Analysis**: The program processes the changes and displays results

3. The application features:
   
   - **GUI Interface**: User-friendly PyQt5 interface for easy navigation
   - **Configuration Management**: Customizable analysis rules via `config.json`
   - **Auto Git Discovery**: Automatic detection of Git repositories
   - **In-App Logging**: Real-time feedback during analysis
   - **Selective Analysis**: Only analyzes changed lines in modified files

## Configuration

The application uses a `config.json` file to customize analysis rules:

```json
{
  "file_encodings": {
    ".cs": "utf-8-sig",
    ".sql": "utf-16le",
    ".py": "utf-8"
  },
  "analysis_checks": {
    "check_line_length": {
      "enabled": true,
      "max_length": 120
    },
    "check_trailing_spaces": {
      "enabled": true,
      "max_trailing_whitespaces": 10
    },
    "check_todo": {
      "enabled": true
    }
  }
}
```

## FAQ

### What can this program be used for?

This program can be used for automatic analysis of Pull Request changes regarding Clean Code principles. It can be stored as a tool in a repository and updated as needed.

**Example:**

You created a Pull Request to merge changes from branch `foo` to `master`. You want to ensure Clean Code guidelines are met so reviewers don't have to focus on these aspects. Run this static code analysis program to get a TODO list containing all Clean Code improvements needed. Copy this list and add it as a comment to your Pull Request, then improve the code and check off items in TFS.

### What can the program check?

The program only analyzes files included in a Pull Request, **not** the entire repository. Currently supported checks include:

| Check               | Description                                                                            |
| ------------------- | -------------------------------------------------------------------------------------- |
| File Encodings      | Verifies correct encoding: `.cs` files in `UTF8-SIG`, `.sql` files in `UTF16-LE`, etc. |
| Unknown Characters  | Detects � characters in code                                                           |
| Maximum Line Length | Ensures lines don't exceed 120 characters (configurable)                               |
| Trailing Whitespace | Checks for excessive trailing spaces (configurable limit)                              |
| TODOs in Code       | Ensures no open TODOs remain in code                                                   |
| Region Formatting   | Ensures proper spacing around `#region` and `#endregion` tags in C# code               |
| Tab Characters      | Detects tab characters in code                                                         |

### Architecture

The application follows an MVC (Model-View-Controller) pattern:

- **Model** (`model.py`): Handles data and business logic
- **View** (`gui.py`): PyQt5 GUI interface
- **Controller** (`controller.py`): Coordinates between model and view
- **Git Integration** (`git.py`): Handles Git repository operations
- **Analysis Engine** (`sca_checks.py`): Performs code quality checks
- **Configuration** (`config_manager.py`): Manages application settings

## Version History

| Date/Version | Changes                                                                                                                                                                            |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 16.06.2025   | Initial version of the program released                                                                                                                                            |
| 03.07.2025   | - GUI implemented<br/>- Config file implemented<br/>- Auto Git Repository Discovery implemented<br/>- In-app logging implemented<br/>- Bugfix: only changed lines are checked<br/> |
| 04.07.2025   | - improved code for analysis<br/>- added feature for automatically selecting master branch as destination<br/>- modernized the gui                                                 |
| 17.07.2025   | - shrinked the gui<br/>- improved gui layout and styling                                                                                                                           |
| 25.07.2025   | - changed gui layout to make it even more compact                                                                                                                                  |