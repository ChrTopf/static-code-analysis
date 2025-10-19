import traceback
from threading import Thread
from typing import List

from analysis import Analysis
from config_parser import ConfigParser
from git_assistant import GitAssistant
from gui.adapter.analysis_complete import AnalysisCompleteAdapter
from logger import Logger
from models.analysis_arguments import AnalysisArguments
from models.file_analysis_result import FileAnalysisResult
from models.repository_info import RepositoryInfo


class MainModel:
    def __init__(self, logger: Logger, config_parser: ConfigParser):
        self.logger = logger
        self.config_parser = config_parser
        self.git_assistant = None
        self.analysis_arguments: AnalysisArguments | None = None
        self.repository_info: RepositoryInfo | None = None
        self.analysis_results: list[FileAnalysisResult] | None = None
        self.is_analyzing = False
        self.analysis_complete_adapter: AnalysisCompleteAdapter | None = None
        self.analysis_thread = None
        
    def prepare(self):
        self.analysis_arguments = self.config_parser.load_analysis_arguments()
        self.git_assistant = GitAssistant(self.analysis_arguments.repository_directory)
        self.__update_repository_info(self.analysis_arguments.repository_directory)
        
    def get_repository_directory(self) -> str:
        return self.analysis_arguments.repository_directory
        
    def set_repository(self, repo_path: str):
        try:
            if self.git_assistant is None:
                self.git_assistant = GitAssistant(repo_path)
            self.analysis_arguments.repository_directory = repo_path
            self.git_assistant.reset_repository_directory(repo_path)
            self.__update_repository_info(repo_path)
        except Exception as e:
            self.analysis_arguments.repository_directory = ""
            self.repository_info = None
            raise Exception(f"Failed to initialize repository: {str(e)}")
    
    def get_repository_info(self) -> RepositoryInfo | None:
        return self.repository_info
    
    def get_initial_source_branch(self) -> str | None:
        if self.analysis_arguments is not None:
            if self.analysis_arguments.source_branch in self.repository_info.branches:
                return self.analysis_arguments.source_branch
        return None
    
    def get_initial_target_branch(self) -> str | None:
        if self.analysis_arguments is not None:
            if self.analysis_arguments.destination_branch in self.repository_info.branches:
                return self.analysis_arguments.destination_branch
        return None
    
    def set_source_branch(self, source_branch: str):
        self.analysis_arguments.source_branch = source_branch
    
    def set_target_branch(self, target_branch: str):
        self.analysis_arguments.destination_branch = target_branch
    
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
            self.analysis = Analysis(self.logger, self.config_parser, self.git_assistant)
            self.analysis_results = self.analysis.execute(self.analysis_arguments)
            self.logger.info("Analysis completed.")
        except Exception as e:
            self.logger.error(f"Analysis failed. Reason:\n{traceback.format_exc()}")
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
            
    def __update_repository_info(self, repository_path: str):
        branches = [b.strip() for b in self.git_assistant.get_local_branches() if b.strip()]
        self.repository_info = RepositoryInfo(
            path=repository_path,
            branches=branches
        )