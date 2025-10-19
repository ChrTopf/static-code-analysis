import os.path

from analysis import Analysis
from config_parser import ConfigParser
from git_assistant import GitAssistant
from logger import Logger
from models.analysis_arguments import AnalysisArguments
from models.cli_arguments import CliArguments
from models.file_analysis_result import FileAnalysisResult
from util.analysis_result_formatter import AnalysisResultFormatter


class HeadlessAnalyzer:
    def __init__(self, logger: Logger, config_parser: ConfigParser):
        self.logger = logger
        self.config_parser = config_parser
        
    def is_configuration_valid(self, cli_arguments: CliArguments) -> bool:
        if cli_arguments.repository is None or len(cli_arguments.repository) == 0:
            self.logger.error("No repository directory specified")
            return False
        if not os.path.isdir(cli_arguments.repository):
            self.logger.error("The specified repository path is not a directory")
            return False
        if cli_arguments.source_branch is None or len(cli_arguments.source_branch) == 0:
            self.logger.error("Source branch is required")
            return False
        if cli_arguments.target_branch is None or len(cli_arguments.target_branch) == 0:
            self.logger.error("Target branch is required")
            return False
        return True
    
    def perform_analysis(self, cli_arguments: CliArguments) -> int:
        analysis_arguments = AnalysisArguments(
            cli_arguments.repository, 
            cli_arguments.source_branch, 
            cli_arguments.target_branch, 
            cli_arguments.changed_lines_only
        )
        self.logger.info(f"Starting analysis: comparing {analysis_arguments.source_branch} against "
                         f"{analysis_arguments.destination_branch}")
        git_assistant = GitAssistant(cli_arguments.repository)
        try:
            analysis = Analysis(self.logger, self.config_parser, git_assistant)
            analysis_results = analysis.execute(analysis_arguments)
            self.logger.info("Analysis completed.")
            return self.__process_analysis_results(analysis_results, cli_arguments.exit_with_code)
        except Exception as e:
            if str(e).__contains__("could not read Username"):
                self.logger.error("Could not authenticate at remote server for fetching the latest changes. If your "
                                  "repository is on github, please try setting up ssh keys! You can test your "
                                  "configuration by executing 'git fetch -v -- origin'. If you are not prompted for "
                                  "a password anymore, this error should disappear.")
            else:
                self.logger.error(e)
            return 3
        
    def __process_analysis_results(self, results: list[FileAnalysisResult], exit_with_code: bool) -> int:
        print(AnalysisResultFormatter.build_result_text(results))
        if self.__has_issues(results) and exit_with_code:
            return 1
        else:
            return 0
        
    def __has_issues(self, results: list[FileAnalysisResult]) -> bool:
        return len([result for result in results if result.has_issues()]) > 0