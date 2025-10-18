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
        self.set_repository_command = None
        self.start_analysis_command = None
        
    def register_commands(self):
        self.set_repository_command = SetRepositoryCommand(self.logger, self.model, self.view)
        self.view.get_repository_section().get_select_repository_button().clicked.connect(
            self.set_repository_command.execute
        )
        self.start_analysis_command = StartAnalysis(self.logger, self.model, self.view)
        self.view.get_run_analysis_button().clicked.connect(self.start_analysis_command.execute)
        self.logger.debug("All commands have been registered")
        
    def register_subscriptions(self):
        analysis_complete_adapter = AnalysisCompleteAdapter(self.view)
        self.model.subscribe_analysis_complete(analysis_complete_adapter)
        self.logger.debug("All subscriptions have been registered")

    def initialize_application(self):
        try:
            self.model.prepare()
            self.view.get_repository_section().update_repository_info(self.model.get_repository_info())
            self.view.get_repository_section().select_source_branch(self.model.get_initial_source_branch())
            self.view.get_repository_section().select_target_branch(self.model.get_initial_target_branch())
        except Exception as e:
            self.logger.error(str(e))
        self.logger.info("Static Code Analysis Tool started")