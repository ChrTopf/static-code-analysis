from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox
)

from gui.themeable import Themeable
from gui.view.repository_section import RepositorySection
from gui.view.result_section import ResultSection


class MainView(QWidget, Themeable):
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
        self.apply_theme(self.__get_dark_theme_variables())
        
    def get_repository_section(self) -> RepositorySection:
        return self.repository_selection

    def get_run_analysis_button(self) -> QPushButton:
        return self.run_button
    
    def get_result_section(self) -> ResultSection:
        return self.result_section

    def set_analysis_running(self, is_running: bool):
        """Update UI to reflect analysis state"""
        self.run_button.setEnabled(not is_running)
        if is_running:
            self.run_button.setText("Analysis Running...")
        else:
            self.run_button.setText("Run Static Code Analysis")

    def __init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(4, 4, 4, 4)
        
        main_layout.addLayout(self.__create_title_layout())
        
        self.repository_selection = RepositorySection()
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

        # Theme toggle
        self.theme_toggle = QCheckBox("Dark Mode")
        self.theme_toggle.setChecked(self.is_dark_mode)
        self.theme_toggle.stateChanged.connect(self.__toggle_theme)
        
        title_layout.addStretch()
        title_layout.addWidget(self.theme_toggle)
        return title_layout
    
    def __get_title_style(self) -> str:
        return """
            #title {
                color: $primary;
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
                background-color: $primary;
                color: $light;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                margin: 4px 0;
            }
            
            #run_button:hover {
                background-color: $secondary;
            }
            
            #run_button:pressed {
                background-color: $secondary;
            }
            
            #run_button:disabled {
                background-color: $dark;
                color: $light;
            }
        """

    def log(self, message, level="INFO"):
        self.result_section.log(message, level)
    
    def __toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = self.theme_toggle.isChecked()
        if self.is_dark_mode:
            self.apply_theme(self.__get_dark_theme_variables())
        else:
            self.apply_theme(self.__get_light_theme_variables())
    
    def apply_theme(self, variables: dict[str, str]):
        self.setStyleSheet(self._replace_theme_variables(variables, self.__get_default_style()))
        
    def __get_default_style(self):
        """Get dark theme stylesheet"""
        return """
            QWidget {
                background-color: $body-bg;
                color: $dark;
                font-family: Arial, sans-serif;
            }
            
            QCheckBox {
                color: $dark;
                font-weight: bold;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid $dark;
                border-radius: 3px;
                background-color: $body-bg-dark;
            }
            
            QCheckBox::indicator:checked {
                background-color: $primary;
                border-color: $primary;
            }
            
            QCheckBox::indicator:checked:before {
                color: $dark;
                font-weight: bold;
            }
            
            QSplitter::handle {
                background-color: $body-bg-light;
                height: 3px;
            }
            
            QSplitter::handle:hover {
                background-color: $primary;
            }
            
            QTabWidget::pane {
                border: 1px solid $body-bg-light;
                border-radius: 4px;
                background-color: $body-bg;
            }
            
            QTabBar::tab {
                background-color: $body-bg-light;
                color: $dark;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: $primary;
                color: $dark;
            }
            
            QTabBar::tab:hover {
                background-color: $primary;
            }
        """
    
    def __get_dark_theme_variables(self) -> dict[str, str]:
        return {
            "$primary": "#9e0000",
            "$secondary": "#884600",
            "$success": "#00c100",
            "$light": "#000000",
            "$dark": "#e1e1e1",
            "$body-bg-light": "#262626",
            "$body-bg-dark": "#101010",
            "$body-bg": "#1a1a1a"
        }
    
    def __get_light_theme_variables(self) -> dict[str, str]:
        return {
            "$primary": "#ea0000",
            "$secondary": "#ffa115",
            "$success": "#00c100",
            "$light": "#ffffff",
            "$dark": "#000000",
            "$body-bg-light": "#ffffff",
            "$body-bg-dark": "#e0e0e0",
            "$body-bg": "#fefefe"
        }
