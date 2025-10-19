import argparse
from dataclasses import dataclass


@dataclass
class CliArguments:
    def __init__(self, parsed_arguments: argparse.Namespace):
        self.headless: bool = parsed_arguments.headless
        self.repository: str = parsed_arguments.repository
        self.source_branch: str = parsed_arguments.source_branch
        self.target_branch: str = parsed_arguments.target_branch
        self.changed_lines_only: bool = not parsed_arguments.all_lines
        self.quiet: bool = parsed_arguments.quiet
        self.exit_with_code: bool = parsed_arguments.exit_with_code
        