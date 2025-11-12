from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox, QCheckBox

from gui.themeablewidget import ThemeableWidget
from models.repository_info import RepositoryInfo


class RepositorySection(QFrame, ThemeableWidget):
    def __init__(self):
        super().__init__()
        self.dir_button = None
        self.dir_label = None
        self.source_branch = None
        self.dest_branch = None
        self.changed_lines_only_checkbox = None
        
        self.setObjectName("section_frame")
        repo_layout = QVBoxLayout()

        repo_header = QLabel("Repository and Branch Selection")
        repo_header.setObjectName("section_header")
        repo_header.setFont(QFont("Arial", 12, QFont.Bold))
        repo_layout.addWidget(repo_header)

        self.repository_selection = self.__create_repository_selection()
        repo_layout.addLayout(self.repository_selection)

        self.branch_selection = self.__create_branch_selection()
        repo_layout.addLayout(self.branch_selection)
        
        additional_settings_section = self.__create_additional_settings_section()
        repo_layout.addLayout(additional_settings_section)

        self.setLayout(repo_layout)
        
    def get_stylesheet(self) -> str:
        return """
            #section_frame {
                background-color: $body-bg;
                border: 1px solid $body-bg-light;
                border-radius: 5px;
                margin: 3px 0;
            }
            
            #section_header {
                color: $dark;
                margin-bottom: 2px;
                background-color: transparent;
            }
        """ + "\n" + self.__get_repository_selection_style() + "\n" + self.__get_branch_selection_style()
    
    def __create_branch_selection(self) -> QHBoxLayout:
        # Branch selection section
        branches_vbox = QVBoxLayout()

        # Source branch
        source_label = QLabel("Source Branch")
        source_label.setFont(QFont("Arial", 8))
        source_label.setObjectName("branch_label")
        branches_vbox.addWidget(source_label)
        self.source_branch = QComboBox()
        self.source_branch.setObjectName("modern_combo")
        self.source_branch.setFont(QFont("Arial", 10))
        self.source_branch.addItems(["main", "develop", "feature-xyz"])
        branches_vbox.addWidget(self.source_branch)

        # Destination branch
        dest_label = QLabel("Target Branch")
        dest_label.setFont(QFont("Arial", 8))
        dest_label.setObjectName("branch_label")
        branches_vbox.addWidget(dest_label)
        self.dest_branch = QComboBox()
        self.dest_branch.setObjectName("modern_combo")
        self.dest_branch.setFont(QFont("Arial", 10))
        self.dest_branch.addItems(["main", "develop", "feature-xyz"])
        branches_vbox.addWidget(self.dest_branch)
        
        return branches_vbox
    
    def __get_branch_selection_style(self) -> str:
        return """
            #branch_label {
                color: $dark;
                background-color: transparent;
            }
        
            #modern_combo {
                background-color: $body-bg;
                border: 2px solid $body-bg-light;
                border-radius: 4px;
                padding: 4px;
                color: $dark;
            }
            
            #modern_combo:focus {
                border-color: $body-bg-light;
            }
            
            #modern_combo QAbstractItemView {
                background-color: $body-bg-light;
                color: $dark;
                selection-background-color: $secondary;
                selection-color: $dark;
            }
        """
    
    def __create_repository_selection(self) -> QHBoxLayout:
        dir_layout = QHBoxLayout()
        self.dir_button = QPushButton("Select Repository")
        self.dir_button.setObjectName("primary_button")
        self.dir_label = QLabel("No repository selected")
        self.dir_label.setObjectName("path_label")
        dir_layout.addWidget(self.dir_button)
        dir_layout.addWidget(self.dir_label, 1)
        dir_layout.setObjectName("repo_selection")
        return dir_layout
    
    def __get_repository_selection_style(self) -> str:
        return """
            #primary_button {
                background-color: $primary;
                color: $dark;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            
            #primary_button:hover {
                background-color: $secondary;
            }
            
            #primary_button:pressed {
                background-color: $primary;
            }
            
            #path_label {
                color: $dark;
                font-style: italic;
                padding: 3px 6px;
                background-color: $body-bg;
                border-radius: 4px;
            }
        """
    
    def __create_additional_settings_section(self) -> QVBoxLayout:
        settings_layout = QVBoxLayout()
        self.changed_lines_only_checkbox = QCheckBox("Analyze changed lines only")
        settings_layout.addWidget(self.changed_lines_only_checkbox)
        return settings_layout
    
    def get_source_branch_selection(self) -> QComboBox:
        return self.source_branch
    
    def get_target_branch_selection(self) -> QComboBox:
        return self.dest_branch

    def get_selected_source_branch(self):
        return self.source_branch.currentText()

    def get_selected_target_branch(self):
        return self.dest_branch.currentText()
    
    def select_source_branch(self, source_branch: str):
        self.source_branch.setCurrentText(source_branch)
        
    def select_target_branch(self, target_branch: str):
        self.dest_branch.setCurrentText(target_branch)

    def get_select_repository_button(self) -> QPushButton:
        return self.dir_button
    
    def get_changed_lines_only_checkbox(self) -> QCheckBox:
        return self.changed_lines_only_checkbox

    def update_repository_path(self, repository_path):
        self.dir_label.setText(repository_path)

    def update_repository_info(self, repo_info: RepositoryInfo):
        self.dir_label.setText(repo_info.path)
        self.source_branch.clear()
        self.source_branch.addItems(repo_info.branches)
        self.dest_branch.clear()
        self.dest_branch.addItems(repo_info.branches)
    
    def select_master_as_target_branch(self, repo_info: RepositoryInfo):
        main_branches = ['main', 'master']
        for branch in main_branches:
            # search for local master
            if branch in repo_info.branches:
                self.dest_branch.setCurrentText(branch)
                return
            # search for master in origin
            remote_main = f'origin/{branch}'
            if remote_main in repo_info.branches:
                self.dest_branch.setCurrentText(branch)
                return
    