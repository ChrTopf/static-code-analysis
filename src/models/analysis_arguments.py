class AnalysisArguments:
    def __init__(self, 
                 repository_directory: str, 
                 source_branch: str, 
                 destination_branch: str, 
                 changed_lines_only: bool):
        self.repository_directory: str = repository_directory
        self.source_branch: str = source_branch
        self.destination_branch: str = destination_branch
        self.changed_lines_only: bool = changed_lines_only