from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox
)

from gui.themeablewidget import ThemeableWidget
from gui.view.repository_section import RepositorySection
from gui.view.result_section import ResultSection


class MainView(ThemeableWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Static Code Analysis")
        self.setGeometry(100, 100, 500, 400)
        self.theme_toggle = None
        self.repository_section: RepositorySection = None
        self.run_button = None
        self.result_section: ResultSection = None
        self.__init_ui()
        self.repaint()
        
    def get_repository_section(self) -> RepositorySection:
        return self.repository_section

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
        
        self.repository_section = RepositorySection()
        main_layout.addWidget(self.repository_section)

        # Analysis button
        self.run_button = self.__create_run_button()
        main_layout.addWidget(self.run_button)

        # Results section using tabs
        self.result_section = ResultSection()
        main_layout.addWidget(self.result_section)
        
        self.setObjectName("main_layout")
        self.setLayout(main_layout)
        
    def __create_title_layout(self) -> QHBoxLayout:
        # Title and theme toggle
        title_layout = QHBoxLayout()

        # Theme toggle
        self.theme_toggle = QCheckBox("Dark Mode")
        self.theme_toggle.setChecked(self._is_dark_mode)
        self.theme_toggle.stateChanged.connect(self.__toggle_theme)
        
        title_layout.addStretch()
        title_layout.addWidget(self.theme_toggle)
        return title_layout
    
    def __get_title_style(self) -> str:
        return """
            #main_layout {
                background-color: $body-bg-dark;
                color: $dark;
                font-family: Arial, sans-serif;
            }
        
            #title {
                color: $primary;
                padding: 4px 0;
            }
        """
    
    def __create_run_button(self) -> QPushButton:
        run_button = QPushButton("Run Static Code Analysis")
        run_button.setObjectName("run_button")
        run_button.setFont(QFont("Arial", 20, QFont.Bold))
        return run_button
    
    def __get_run_button_style(self) -> str:
        return """
            #run_button {
                background-color: $primary;
                color: $dark;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 20px;
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
        self.apply_theme(self.theme_toggle.isChecked())
            
    def get_stylesheet(self) -> str:
        return self.__get_title_style() + "\n" + self.__get_run_button_style()
    