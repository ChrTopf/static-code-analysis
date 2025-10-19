class AnalysisConfig:
    def __init__(self, 
                 forbidden_files: list[str],
                 ignored_files: list[str],
                 file_encodings: dict[str, str], 
                 standard_checks: dict[str, object], 
                 specific_checks: dict[str, dict[str, object]]):
        self.forbidden_files: list[str] = forbidden_files
        self.ignored_files: list[str] = ignored_files
        self.file_encodings: dict[str, str] = file_encodings
        self.standard_checks: dict[str, object] = standard_checks
        self.specific_checks: dict[str, dict[str, object]] = specific_checks
        