from abc import abstractmethod, ABC

from models.line_analysis_issue import LineAnalysisIssue
from models.loaded_file import LoadedFile


class Check(ABC):
    @abstractmethod
    def parse_config(self, config_object: dict[str, object] | None):
        pass

    @abstractmethod
    def execute_on_changed_file(self, changed_file: LoadedFile) -> list[LineAnalysisIssue]:
        pass