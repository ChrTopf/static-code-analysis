from gui.adapter.analysis_complete import AnalysisCompleteAdapter
from gui.commands.set_repository import SetRepositoryCommand
from gui.commands.start_analysis import StartAnalysis
from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger

class MainController:
    def __init__(self, model: MainModel, view: MainView, logger: Logger):
        self.model = model
        self.logger = logger
        self.view = view
        
    def initialize_application(self):
        self.logger.info("Static Code Analysis Tool started")
        
    def register_commands(self):
        set_repository_command = SetRepositoryCommand(self.logger, self.model, self.view)
        self.view.get_repository_section().get_select_repository_button().clicked.connect(
            set_repository_command.execute
        )
        start_analysis_command = StartAnalysis(self.logger, self.model, self.view)
        self.view.get_run_analysis_button().clicked.connect(start_analysis_command.execute)
        
    def register_subscriptions(self):
        analysis_complete_adapter = AnalysisCompleteAdapter(self.view)
        self.model.subscribe_analysis_complete(analysis_complete_adapter)
        pass