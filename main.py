import sys
from PyQt5.QtWidgets import QApplication

from analysis import Analysis
from config_parser import ConfigParser
from git_assistant import GitAssistant
from gui.main_controller import MainController

from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger

class StaticCodeAnalysisApp:
    def __init__(self):
        self.logger = Logger()
        self.config_parser = ConfigParser()
        self.analysis_arguments = self.config_parser.load_analysis_arguments()
        # TODO: auto detect repository
        self.git_assistant = GitAssistant(self.analysis_arguments.repository_directory)
        self.analysis = Analysis(self.logger, self.config_parser, self.git_assistant)
        
        # prepare the gui
        self.app = QApplication(sys.argv)
        # Create MVC components
        self.view = MainView()
        self.model = MainModel(self.logger, self.config_parser, self.git_assistant, self.analysis)
        self.controller = MainController(self.model, self.view, self.logger)
        self.controller.initialize_application()
        self.controller.register_commands()
        self.controller.register_subscriptions()
        
    def run(self):
        """Start the application"""
        self.view.show()
        
        # Initialize application through controller
        self.controller.initialize_application()
        
        return self.app.exec_()

if __name__ == "__main__":
    app = StaticCodeAnalysisApp()
    sys.exit(app.run())
