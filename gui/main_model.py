from typing import List, Optional

from analysis import Analysis
from git_assistant import GitAssistant
from gui.adapter.analysis_complete import AnalysisCompleteAdapter
from logger import Logger
from models.analysis_arguments import AnalysisArguments
from models.file_analysis_result import FileAnalysisResult
from models.repository_info import RepositoryInfo


class MainModel:
    def __init__(self, 
                 logger: Logger, 
                 analysis_arguments: AnalysisArguments, 
                 git_assistant: GitAssistant, 
                 analysis: Analysis):
        self.logger = logger
        self.analysis_arguments = analysis_arguments
        self.git_assistant = git_assistant
        self.analysis = analysis
        self.repo_directory: Optional[str] = None
        self.repository_info: Optional[RepositoryInfo] = None
        self.analysis_results: list[FileAnalysisResult] | None = None
        self.is_analyzing = False
        self.analysis_complete_adapter: AnalysisCompleteAdapter | None = None
        
    def set_repository(self, repo_path: str) -> bool:
        try:
            self.repo_directory = repo_path
            self.git_assistant.reset_repository_directory(repo_path)
            # Get branch information
            branches = [b.strip() for b in self.git_assistant.get_local_branches() if b.strip()]
            self.repository_info = RepositoryInfo(
                path=repo_path,
                local_branches=branches,
                remote_branches=branches
            )
            return True
        except Exception as e:
            self.repo_directory = None
            self.repository_info = None
            raise Exception(f"Failed to initialize repository: {str(e)}")
    
    def get_repository_info(self) -> Optional[RepositoryInfo]:
        return self.repository_info
    
    def start_analysis(self):
        if self.is_analyzing:
            self.logger.warn("The analysis is already running.")
            return
        
        self.is_analyzing = True
        self.analysis_results = None
        
        try:
            self.analysis_results = self.analysis.execute(self.analysis_arguments)
            self.logger.info("Analysis completed.")
        except Exception as e:
            self.logger.error(f"Analysis failed. Reason: {str(e)}")
        finally:
            self.__notify_analysis_complete(self.analysis_results)
            self.is_analyzing = False
    
    def get_analysis_results(self) -> List[FileAnalysisResult]:
        return self.analysis_results
    
    def is_analysis_running(self) -> bool:
        return self.is_analyzing
    
    def subscribe_analysis_complete(self, analysis_complete_adapter: AnalysisCompleteAdapter):
        self.analysis_complete_adapter = analysis_complete_adapter
    
    def __notify_analysis_complete(self, result: list[FileAnalysisResult] | None):
        if self.analysis_complete_adapter:
            self.analysis_complete_adapter.on_signal_received(result)