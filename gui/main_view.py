from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QCheckBox
)

from gui.view.repository_selection import RepositorySelection
from gui.view.result_section import ResultSection


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Static Code Analysis")
        self.setGeometry(100, 100, 500, 400)
        self.is_dark_mode = True
        self.theme_toggle = None
        self.repository_selection = None
        self.run_button = None
        self.result_section = None
        self.__init_ui()
        self.__apply_theme()
        
    def get_repository_selection(self) -> RepositorySelection:
        return self.repository_selection

    def get_run_analysis_button(self) -> QPushButton:
        return self.run_button
    
    def get_result_section(self) -> ResultSection:
        return self.result_section

    def __init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(4, 4, 4, 4)
        
        main_layout.addLayout(self.__create_title_layout())
        
        self.repository_selection = RepositorySelection()
        main_layout.addWidget(self.repository_selection)

        # Analysis button
        self.run_button = self.__create_run_button()
        main_layout.addWidget(self.run_button)

        # Results section using tabs
        self.result_section = ResultSection()
        main_layout.addWidget(self.result_section)
        
        self.setLayout(main_layout)
        
    def __create_title_layout(self) -> QHBoxLayout:
        # Title and theme toggle
        title_layout = QHBoxLayout()
        title_label = QLabel("Static Code Analysis Tool")
        title_label.setObjectName("title")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))

        # Theme toggle
        self.theme_toggle = QCheckBox("Dark Mode")
        self.theme_toggle.setChecked(self.is_dark_mode)
        self.theme_toggle.stateChanged.connect(self.__toggle_theme)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.theme_toggle)
        return title_layout
    
    def __get_title_style(self) -> str:
        return """
            #title {
                color: #4fc3f7;
                padding: 4px 0;
            }
        """
    
    def __create_run_button(self) -> QPushButton:
        run_button = QPushButton("▶ Run Static Code Analysis")
        run_button.setObjectName("run_button")
        run_button.setFont(QFont("Arial", 13, QFont.Bold))
        return run_button
    
    def __get_run_button_style(self) -> str:
        return """
            #run_button {
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                margin: 4px 0;
            }
            
            #run_button:hover {
                background-color: #45a049;
            }
            
            #run_button:pressed {
                background-color: #388e3c;
            }
            
            #run_button:disabled {
                background-color: #666666;
                color: #999999;
            }
        """

    def log(self, message, level="INFO"):
        color_map = {
            "INFO": "green",
            "WARNING": "orange",
            "ERROR": "red",
            "DEBUG": "purple"
        }

        color = color_map.get(level.upper(), "black")
        formatted_message = f'<span style="color:{color};"><b>[{level.upper()}]</b> {message}</span>'

        self.console.moveCursor(QTextCursor.End)
        self.console.insertHtml(formatted_message + "<br>")
        self.console.moveCursor(QTextCursor.End)
    
    def __toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = self.theme_toggle.isChecked()
        self.__apply_theme()
    
    def __apply_theme(self):
        self.setStyleSheet(self.__get_default_style())
    
    def __get_default_style(self):
        """Get dark theme stylesheet"""
        return """
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            
            QCheckBox {
                color: #ffffff;
                font-weight: bold;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #666666;
                border-radius: 3px;
                background-color: #404040;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4fc3f7;
                border-color: #4fc3f7;
            }
            
            QCheckBox::indicator:checked:before {
                content: "✓";
                color: #000000;
                font-weight: bold;
            }
            
            QSplitter::handle {
                background-color: #555555;
                height: 3px;
            }
            
            QSplitter::handle:hover {
                background-color: #4fc3f7;
            }
            
            QTabWidget::pane {
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #3c3c3c;
            }
            
            QTabBar::tab {
                background-color: #555555;
                color: #ffffff;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #4fc3f7;
                color: #000000;
            }
            
            QTabBar::tab:hover {
                background-color: #666666;
            }
        """
    
    def __get_dark_theme_variables(self) -> dict[str, str]:
        return {
            "$primary": "#4fc3f7"
        }
    
    def __get_light_theme_variables(self) -> dict[str, str]:
        return {
            "$primary": "#4fc3f7"
        }
