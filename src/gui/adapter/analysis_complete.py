from PyQt5.QtCore import QObject, pyqtSignal

from gui.adapter.adapter import Adapter
from gui.main_view import MainView
from logger import Logger
from models.file_analysis_result import FileAnalysisResult


class AnalysisCompleteAdapter(Adapter, QObject):
    analysis_completed = pyqtSignal(object)

    def __init__(self, logger: Logger, view: MainView):
        Adapter.__init__(self, view)
        QObject.__init__(self)
        self.logger = logger
        self.analysis_completed.connect(self.__handle_analysis_complete)
        
    def on_signal_received(self, results: list[FileAnalysisResult] | None):
        self.analysis_completed.emit(results)

    def __handle_analysis_complete(self, results: list[FileAnalysisResult]):
        self.view.get_result_section().show_analysis_results(results)
        self.view.set_analysis_running(False)