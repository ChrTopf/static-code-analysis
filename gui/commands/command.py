from abc import abstractmethod

from gui.main_model import MainModel
from gui.main_view import MainView
from logger import Logger


class Command:
    def __init__(self, logger: Logger, model: MainModel, view: MainView):
        self.logger = logger
        self.model = model
        self.view = view
        
    @abstractmethod
    def execute(self):
        pass