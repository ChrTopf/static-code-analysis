from gui.commands.command import Command
from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger


class SetSourceBranch(Command):
    def __init__(self, logger: Logger, model: MainModel, view: MainView):
        super().__init__(logger, model, view)
        
    def execute(self):
        source_branch = self.view.get_repository_section().get_selected_source_branch()
        self.model.set_source_branch(source_branch)