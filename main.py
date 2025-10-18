import sys

from PyQt5.QtWidgets import QApplication

from config_parser import ConfigParser
from gui.main_controller import MainController
from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger


class StaticCodeAnalysisApp:
    def __init__(self):
        self.logger = Logger()
        self.config_parser = ConfigParser()
        
    def run(self) -> int:      
        return self.__run_gui()
    
    def __run_gui(self):
        self.app = QApplication(sys.argv)
        # Create MVC components
        self.view = MainView()
        self.model = MainModel(self.logger, self.config_parser)
        self.controller = MainController(self.model, self.view, self.logger)
        self.controller.register_commands()
        self.controller.register_subscriptions()
        self.controller.initialize_application()
        self.view.show()
        return self.app.exec_()

if __name__ == "__main__":
    app = StaticCodeAnalysisApp()
    sys.exit(app.run())
