from abc import abstractmethod

from gui.main_view import MainView


class Adapter:
    def __init__(self, view: MainView):
        self.view = view
        
    @abstractmethod
    def on_signal_received(self):
        pass