from PyQt5.QtWidgets import QFileDialog

from gui.commands.command import Command
from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger


class SetRepositoryCommand(Command):
    def __init__(self, logger: Logger, model: MainModel, view: MainView):
        super().__init__(logger, model, view)
        
    def execute(self):
        # TODO: get current repository path from the model
        # TODO: set default path for file open dialog
        directory = QFileDialog.getExistingDirectory(self.view, "Select Directory")
        if directory:
            self.model.set_repository(directory)
            self.view.update_repository_path(directory)
            repository_info = self.model.get_repository_info()
            self.view.update_repository_info(repository_info)