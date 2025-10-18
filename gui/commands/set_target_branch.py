from gui.commands.command import Command
from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger


class SetTargetBranch(Command):
    def __init__(self, logger: Logger, model: MainModel, view: MainView):
        super().__init__(logger, model, view)
        
    def execute(self):
        target_branch = self.view.get_repository_section().get_selected_target_branch()
        self.model.set_target_branch(target_branch)