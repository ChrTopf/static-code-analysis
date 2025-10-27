import glob
import os.path

from analysis_config import AnalysisConfig
from analysis_exception import AnalysisException
from config_parser import ConfigParser
from file_analyzer import FileAnalyzer
from git_assistant import GitAssistant
from logger import Logger
from models.analysis_arguments import AnalysisArguments
from models.changed_file import ChangedFile
from models.file_analysis_result import FileAnalysisResult
from models.line_analysis_issue import LineAnalysisIssue


class Analysis:
    def __init__(self, logger: Logger, config_parser: ConfigParser, git_assistant: GitAssistant):
        self.__logger = logger
        self.__config_parser = config_parser
        self.__git_assistant = git_assistant
        self.__analysis_config_name = "analysis_config.json5"
        
    def execute(self, analysis_arguments: AnalysisArguments) -> list[FileAnalysisResult]:
        self.__logger.info("The static code analysis has been started.")
        self.__verify_arguments(analysis_arguments)
        analysis_config = self.__get_analysis_config(analysis_arguments)
        changed_files = self.__load_changed_files(analysis_arguments)
        return self.__analyze_all_files(analysis_config, changed_files)
    
    def __verify_arguments(self, analysis_arguments: AnalysisArguments):
        if analysis_arguments.repository_directory is None or len(analysis_arguments.repository_directory) == 0:
            raise ValueError("The repository directory cannot be empty.")
        if analysis_arguments.source_branch is None or len(analysis_arguments.source_branch) == 0:
            raise ValueError("The source branch is cannot be empty.")
        if analysis_arguments.destination_branch is None or len(analysis_arguments.destination_branch) == 0:
            raise ValueError("The destination branch is cannot be empty.")
    
    def __load_changed_files(self, analysis_arguments: AnalysisArguments) -> list[ChangedFile]:
        self.__logger.info("Loading changed files...")
        if analysis_arguments.source_branch == analysis_arguments.destination_branch:
            return self.__load_all_files_in_directory(analysis_arguments.repository_directory)
        else:
            return self.__load_changed_files_from_diff(analysis_arguments)
        
    def __load_all_files_in_directory(self, path: str) -> list[ChangedFile]:
        return [ChangedFile(os.path.join(dp, f), None, True) 
                for dp, dn, filenames in os.walk(path) for f in filenames 
                if not dp.__contains__(".git")]
    
    def __load_changed_files_from_diff(self, analysis_arguments: AnalysisArguments) -> list[ChangedFile]:
        self.__git_assistant.reset_repository_directory(analysis_arguments.repository_directory)
        return self.__git_assistant.get_changes_of_pull_request(
            analysis_arguments.source_branch,
            analysis_arguments.destination_branch,
            analysis_arguments.changed_lines_only
        )
    
    def __get_analysis_config(self, analysis_arguments: AnalysisArguments) -> AnalysisConfig:
        self.__logger.info("Loading analysis config...")
        file_path = self.__find_analysis_config(analysis_arguments.repository_directory)
        return self.__config_parser.load_analysis_config(file_path)
    
    def __find_analysis_config(self, search_directory: str) -> str:
        matching_file_paths = glob.glob(f"{search_directory}/**/{self.__analysis_config_name}", recursive=True)
        if len(matching_file_paths) > 1:
            raise Exception(f"Multiple analysis configs found in '{search_directory}'. Please make sure that there is "
                            f"only one '{self.__analysis_config_name}' present.")
        elif len(matching_file_paths) == 1:
            return matching_file_paths[0]
        elif os.path.isfile(self.__analysis_config_name):
            return self.__analysis_config_name
        else:
            raise FileNotFoundError(f"File not found: '{self.__analysis_config_name}'. Please put that file in the "
                                    f"repository to be analyzed or next to the executable of the static code analysis "
                                    f"tool.")
    
    def __analyze_all_files(self, analysis_config: AnalysisConfig, changed_files: list[ChangedFile]) \
            -> list[FileAnalysisResult]:
        self.__logger.info(f"Analyzing {len(changed_files)} changed files...")
        file_analyzer = FileAnalyzer(analysis_config, self.__git_assistant.get_repository_directory())
        results = []
        for changed_file in changed_files:
            self.__logger.info(f"Analyzing changed file: {changed_file.file_path}")
            results.append(self.__perform_analysis_on_file(file_analyzer, changed_file))
        self.__logger.info("Static code analysis completed.")
        return results
    
    def __perform_analysis_on_file(self, file_analyzer: FileAnalyzer, changed_file: ChangedFile) -> FileAnalysisResult:
        try:
            return file_analyzer.analyze_changed_file(changed_file)
        except AnalysisException as analysis_exception:
            result = FileAnalysisResult(changed_file.get_relative_path(self.__git_assistant.get_repository_directory()))
            result.issues.append(LineAnalysisIssue(0, str(analysis_exception)))
            return result
        