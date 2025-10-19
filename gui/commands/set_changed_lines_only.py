from gui.commands.command import Command
from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger


class SetChangedLinesOnly(Command):
    def __init__(self, logger: Logger, model: MainModel, view: MainView):
        super().__init__(logger, model, view)
        
    def execute(self):
        changed_lines_only = self.view.repository_section.get_changed_lines_only_checkbox().isChecked()
        self.model.set_changed_lines_only(changed_lines_only)
        