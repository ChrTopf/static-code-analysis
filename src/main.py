import sys

from PyQt5.QtWidgets import QApplication

from cli_argument_parser import CliArgumentParser
from config_parser import ConfigParser
from gui.main_controller import MainController
from gui.main_model import MainModel
from gui.main_view import MainView
from headless_analyzer import HeadlessAnalyzer
from logger import Logger


class StaticCodeAnalysisApp:
    def __init__(self):
        self.cli_args = CliArgumentParser()
        self.arguments = self.cli_args.get_parsed_arguments()
        self.logger = Logger(self.arguments.quiet)
        self.config_parser = ConfigParser()
        
    def run(self) -> int:
        if self.arguments.headless:
            return self.__run_headless()
        else:    
            return self.__run_gui()
        
    def __run_headless(self) -> int:
        self.headless_analyzer = HeadlessAnalyzer(self.logger, self.config_parser)
        if not self.headless_analyzer.is_configuration_valid(self.arguments):
            return 2
        else:
            return self.headless_analyzer.perform_analysis(self.arguments)
    
    def __run_gui(self):
        self.app = QApplication(sys.argv)
        # Create MVC components
        self.view = MainView()
        self.logger.set_gui(self.view)
        self.model = MainModel(self.logger, self.config_parser)
        self.controller = MainController(self.model, self.view, self.logger)
        self.controller.initialize_application()
        self.controller.register_commands()
        self.controller.register_subscriptions()
        self.view.show()
        return self.app.exec_()

if __name__ == "__main__":
    app = StaticCodeAnalysisApp()
    sys.exit(app.run())
