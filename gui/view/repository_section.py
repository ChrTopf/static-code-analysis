from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox

from gui.themeable import Themeable
from models.repository_info import RepositoryInfo


class RepositorySection(QFrame, Themeable):
    def __init__(self):
        super().__init__()
        self.dir_button = None
        self.dir_label = None
        self.source_branch = None
        self.dest_branch = None
        
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

        self.setLayout(repo_layout)
        
    def __get_style(self) -> str:
        return """
            #section_frame {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 5px;
                margin: 3px 0;
            }
            
            #section_header {
                color: #ffffff;
                margin-bottom: 2px;
                background-color: transparent;
            }
        """ + "\n" + self.__get_repository_selection_style() + "\n" + self.__get_branch_selection_style()
    
    def __create_branch_selection(self) -> QHBoxLayout:
        # Branch selection section
        branches_grid = QHBoxLayout()

        # Source branch
        source_col = QVBoxLayout()
        source_label = QLabel("Source Branch")
        source_label.setFont(QFont("Arial", 8))
        source_label.setObjectName("branch_label")
        source_col.addWidget(source_label)
        self.source_branch = QComboBox()
        self.source_branch.setObjectName("modern_combo")
        self.source_branch.setFont(QFont("Arial", 10))
        self.source_branch.addItems(["main", "develop", "feature-xyz"])
        source_col.addWidget(self.source_branch)

        # Destination branch
        dest_col = QVBoxLayout()
        dest_label = QLabel("Destination Branch")
        dest_label.setFont(QFont("Arial", 8))
        dest_label.setObjectName("branch_label")
        dest_col.addWidget(dest_label)
        self.dest_branch = QComboBox()
        self.dest_branch.setObjectName("modern_combo")
        self.dest_branch.setFont(QFont("Arial", 10))
        self.dest_branch.addItems(["main", "develop", "feature-xyz"])
        dest_col.addWidget(self.dest_branch)

        branches_grid.addLayout(source_col)
        branches_grid.addLayout(dest_col)
        return branches_grid
    
    def __get_branch_selection_style(self) -> str:
        return """
            #branch_label {
                color: #ffffff;
                background-color: transparent;
            }
        
            #modern_combo {
                background-color: #404040;
                border: 2px solid #666666;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
            }
            
            #modern_combo:focus {
                border-color: #4fc3f7;
            }
            
            #modern_combo QAbstractItemView {
                background-color: #404040;
                color: #ffffff;
                selection-background-color: #4fc3f7;
                selection-color: #000000;
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
                color: $light;
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
                color: #bbbbbb;
                font-style: italic;
                padding: 3px 6px;
                background-color: #404040;
                border-radius: 4px;
            }
        """
    
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

    def update_repository_path(self, repository_path):
        self.dir_label.setText(repository_path)

    def update_repository_info(self, repo_info: RepositoryInfo):
        """Update UI with repository information"""
        self.dir_label.setText(repo_info.path)

        # Update branch dropdowns
        self.source_branch.clear()
        self.source_branch.addItems(repo_info.local_branches)
        self.dest_branch.clear()
        self.dest_branch.addItems(repo_info.remote_branches)

        # Auto-select main/master branch as default destination if available
        main_branches = ['main', 'master']
        for branch in main_branches:
            # Check remote branches first (with origin/ prefix)
            remote_main = f'origin/{branch}'
            if remote_main in repo_info.remote_branches:
                index = repo_info.remote_branches.index(remote_main)
                self.dest_branch.setCurrentIndex(index)
                break
            # Check local branches
            elif branch in repo_info.local_branches:
                # If found in local but not remote, still select it in dest_branch
                # But first check if the branch exists in remote list
                if branch in repo_info.remote_branches:
                    index = repo_info.remote_branches.index(branch)
                    self.dest_branch.setCurrentIndex(index)
                    break

    def apply_theme(self, theme_variables: dict[str, str]) -> None:
        self.setStyleSheet(self._replace_theme_variables(theme_variables, self.__get_style()))