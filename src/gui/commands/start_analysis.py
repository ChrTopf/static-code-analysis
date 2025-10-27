from gui.commands.command import Command
from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger


class StartAnalysis(Command):
    def __init__(self, logger: Logger, model: MainModel, view: MainView):
        super().__init__(logger, model, view)
        
    def execute(self):
        source_branch = self.view.get_repository_section().get_selected_source_branch()
        target_branch = self.view.get_repository_section().get_selected_target_branch()
        if not source_branch or not target_branch:
            self.logger.error("Please select both source and target branches!")
            return
        
        if len(source_branch) == 0:
            self.logger.error("Please select a source branch!")
            return
        
        if len(target_branch) == 0:
            self.logger.error("Please select a target branch!")
            return

        if self.model.is_analysis_running():
            self.logger.warn("Analysis already in progress!")
            return
        
        self.logger.info(f"Starting analysis: comparing {source_branch} against {target_branch}")
        self.model.save_analysis_arguments()
        self.view.set_analysis_running(True)
        self.view.get_result_section().clear_analysis_results()
        self.model.start_analysis()