from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QTableWidget, QHeaderView, \
    QTabWidget, QTableWidgetItem, QApplication

from gui.themeable import Themeable
from models.file_analysis_result import FileAnalysisResult


class ResultSection(QTabWidget, Themeable):
    def __init__(self):
        super().__init__()
        self.copy_button = None
        self.upper_output = None
        self.problem_table = None
        self.console = None
        
        self.setObjectName("results_tabs")

        self.summary_widget = self.__create_summary_tab()
        self.issues_widget = self.__create_issues_tab()
        self.console_widget = self.__create_console_tab()
        
        self.addTab(self.summary_widget, "Analysis Summary")
        self.addTab(self.issues_widget, "Issues Found")
        self.addTab(self.console_widget, "Console Output")
        
    def __create_summary_tab(self) -> QWidget:
        summary_widget = QWidget()
        summary_layout = QVBoxLayout()
        summary_layout.setContentsMargins(4, 4, 4, 4)

        summary_header_layout = QHBoxLayout()
        self.copy_button = QPushButton("📋 Copy")
        self.copy_button.setObjectName("secondary_button")
        self.copy_button.clicked.connect(self.__copy_upper_output)

        summary_header_layout.addStretch()
        summary_header_layout.addWidget(self.copy_button)

        summary_layout.addLayout(summary_header_layout)
        self.upper_output = QTextEdit()
        self.upper_output.setObjectName("info_output")
        self.upper_output.setFont(QFont("Consolas", 10))
        self.upper_output.setReadOnly(True)
        summary_layout.addWidget(self.upper_output)
        summary_widget.setLayout(summary_layout)
        return summary_widget
    
    def __get_summary_tab_style(self) -> str:
        return """
            #secondary_button {
                background-color: #666666;
                color: #ffffff;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            #secondary_button:hover {
                background-color: #777777;
            }
            
            #info_output {
                background-color: #404040;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
            }
        """
    
    def __create_issues_tab(self) -> QWidget:
        issues_widget = QWidget()
        issues_layout = QVBoxLayout()
        issues_layout.setContentsMargins(4, 4, 4, 4)

        self.problem_table = QTableWidget()
        self.problem_table.setObjectName("modern_table")
        self.problem_table.setColumnCount(3)
        self.problem_table.setHorizontalHeaderLabels(["File", "Line", "Problem"])
        self.problem_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.problem_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.problem_table.setAlternatingRowColors(True)
        self.problem_table.verticalHeader().setVisible(False)

        # Enable scrollbars for the table
        self.problem_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.problem_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.problem_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.problem_table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        # Make table headers resize properly
        header = self.problem_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        issues_layout.addWidget(self.problem_table)
        issues_widget.setLayout(issues_layout)
        return issues_widget
    
    def __get_issues_tab_style(self) -> str:
        return """
            #modern_table {
                background-color: #3c3c3c;
                alternate-background-color: #444444;
                color: #ffffff;
                gridline-color: #555555;
                border: 1px solid #555555;
                border-radius: 4px;
                margin: 2px 0;
            }
            
            #modern_table QHeaderView::section {
                background-color: #4fc3f7;
                color: #000000;
                padding: 4px;
                border: none;
                font-weight: bold;
            }
            
            #modern_table::item:selected {
                background-color: #4fc3f7;
                color: #000000;
            }
        """
    
    def __create_console_tab(self) -> QWidget:
        console_widget = QWidget()
        console_layout = QVBoxLayout()
        console_layout.setContentsMargins(4, 4, 4, 4)

        self.console = QTextEdit()
        self.console.setObjectName("console_output")
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 10))
        console_layout.addWidget(self.console)
        console_widget.setLayout(console_layout)
        return console_widget
    
    def __get_console_tab_style(self) -> str:
        return """
            #console_output {
                background-color: #1e1e1e;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
                font-family: 'Consolas', monospace;
            }
        """

    def __copy_upper_output(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.upper_output.toPlainText())

    def apply_theme(self, theme_variables: dict[str, str]) -> None:
        self.summary_widget.setStyleSheet(self._replace_theme_variables(
            theme_variables, self.__get_summary_tab_style()
        ))
        self.issues_widget.setStyleSheet(self._replace_theme_variables(
            theme_variables, self.__get_issues_tab_style()
        ))
        self.console_widget.setStyleSheet(self._replace_theme_variables(
            theme_variables, self.__get_console_tab_style()
        ))

    def show_analysis_results(self, analysis_results: list[FileAnalysisResult]):
        self.clear_analysis_results()
        if analysis_results is None:
            return
        self.__update_result_text(analysis_results)
        self.__update_result_table(analysis_results)

    def clear_analysis_results(self):
        self.problem_table.setRowCount(0)
        self.upper_output.clear()
        
    def __update_result_text(self, results: list[FileAnalysisResult]):
        results = self.__filter_results_for_issues(results)
        if len(results) > 0:
            result_text = self.__get_result_text_for_issues(results)
        else:
            result_text = "✅ No issues found in changed code"
        self.upper_output.setText(result_text)

    def __filter_results_for_issues(self, results: list[FileAnalysisResult]) -> list[FileAnalysisResult]:
        return [result for result in results if result.has_issues()]
    
    def __get_result_text_for_issues(self, results: list[FileAnalysisResult]) -> str:
        lines = [f"❌ Found {len(results)} issues in changed code"]
        lines += self.__format_issues_for_info_output(results)
        return "\n".join(lines)

    def __format_issues_for_info_output(self, results: list[FileAnalysisResult]) -> list[str]:
        formatted_issues = []
        for result in results:
            formatted_issues.append(f"### File {result.file_path} has {len(result.issues)} issues:")
            prettified_issues = result.get_prettied_issues()
            formatted_issues += [f"- [ ] {issue}" for issue in prettified_issues]
        return formatted_issues
    
    def __update_result_table(self, results: list[FileAnalysisResult]):
        for result in results:
            for issue in result.issues:
                row_position = self.problem_table.rowCount()
                self.problem_table.insertRow(row_position)
                self.problem_table.setItem(row_position, 0, QTableWidgetItem(result.file_path))
                self.problem_table.setItem(row_position, 1, QTableWidgetItem(str(issue.line_number)))
                self.problem_table.setItem(row_position, 2, QTableWidgetItem(issue.issue_description))
        