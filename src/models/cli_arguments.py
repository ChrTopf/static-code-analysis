import argparse
from dataclasses import dataclass


@dataclass
class CliArguments:
    def __init__(self, parsed_arguments: argparse.Namespace):
        self.headless: bool = parsed_arguments.headless
        self.repository: str = parsed_arguments.repository
        self.source_branch: str = parsed_arguments.source_branch
        self.target_branch: str = parsed_arguments.target_branch
        self.changed_lines_only: bool = parsed_arguments.changed_lines_only
        self.verbose: bool = parsed_arguments.verbose
        self.exit_with_code: bool = parsed_arguments.exit_with_code
        