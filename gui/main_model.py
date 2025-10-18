from threading import Thread
from typing import List

from analysis import Analysis
from config_parser import ConfigParser
from git_assistant import GitAssistant
from gui.adapter.analysis_complete import AnalysisCompleteAdapter
from logger import Logger
from models.file_analysis_result import FileAnalysisResult
from models.repository_info import RepositoryInfo


class MainModel:
    def __init__(self, 
                 logger: Logger, 
                 config_parser: ConfigParser, 
                 git_assistant: GitAssistant, 
                 analysis: Analysis):
        self.logger = logger
        self.config_parser = config_parser
        self.analysis_arguments = config_parser.load_analysis_arguments()
        self.git_assistant = git_assistant
        self.analysis = analysis
        self.repository_info: RepositoryInfo = None
        self.analysis_results: list[FileAnalysisResult] | None = None
        self.is_analyzing = False
        self.analysis_complete_adapter: AnalysisCompleteAdapter | None = None
        self.analysis_thread = None
        
    def get_repository_directory(self) -> str:
        return self.analysis_arguments.repository_directory
        
    def set_repository(self, repo_path: str) -> bool:
        try:
            self.analysis_arguments.repository_directory = repo_path
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
            self.analysis_arguments.repository_directory = ""
            self.repository_info = None
            raise Exception(f"Failed to initialize repository: {str(e)}")
    
    def get_repository_info(self) -> RepositoryInfo:
        return self.repository_info
    
    def save_analysis_arguments(self):
        self.config_parser.store_analysis_arguments(self.analysis_arguments)
    
    def start_analysis(self):
        if self.is_analyzing:
            self.logger.warn("The analysis is already running.")
            return
        
        self.is_analyzing = True
        self.analysis_results = None

        self.analysis_thread = Thread(target=self.__analyze_async)
        self.analysis_thread.start()
            
    def __analyze_async(self):
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