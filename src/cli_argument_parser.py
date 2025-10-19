import argparse

from models.cli_arguments import CliArguments


class CliArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="Static Code Analysis",
            description="Tool for performing static code analysis between two branches of a repository. The intended "
                        "use-case for this tool is to automatically check all changes in a pull request.",
            epilog="This tool is developed by ChrTopf and was sponsored by TheHolyException. "
        )
        self.parser.add_argument("-hl", 
                                 "--headless", 
                                 type=bool, 
                                 default=False,
                                 help="Run without graphical user interface.")
        self.parser.add_argument("-r", 
                                 "--repository",
                                 type=str,
                                 default=None,
                                 help="The path to the repository to be analyzed.")
        self.parser.add_argument("-s", 
                                 "--source-branch",
                                 type=str,
                                 default=None,
                                 help="The source branch of the pull request.")
        self.parser.add_argument("-t", 
                                 "--target-branch",
                                 type=str,
                                 default=None,
                                 help="The target branch of the pull request. Usually this should be the master "
                                      "branch.")
        self.parser.add_argument("-c", 
                                 "--changed-lines-only", 
                                 type=bool,
                                 default=True,
                                 help="Set this to false to analyze all lines of the changed files.")
        self.parser.add_argument("-v", 
                                 "--verbose", 
                                 type=bool,
                                 default=False,
                                 help="Set this to true, if you want to see informational and debug output. If set to "
                                      "false, only warnings and errors are printed.")
        self.parser.add_argument("-e", 
                                 "--exit-with-code", 
                                 type=bool,
                                 default=True,
                                 help="Set this to false if you dont want the application to exit with an error if "
                                      "issues were found.")
        
    def get_parsed_arguments(self) -> CliArguments:
        return CliArguments(self.parser.parse_args())