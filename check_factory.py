from analysis_config import AnalysisConfig
from checks.check import Check
from checks.line_length import LineLength
from checks.region_newline import RegionNewline
from checks.replacement_characters import ReplacementCharacters
from checks.tabs import Tabs
from checks.todo import TODO
from checks.trailing_whitespace import TrailingWhitespace


class CheckFactory:
    def __init__(self, analysis_config: AnalysisConfig):
        self.analysis_config = analysis_config
        self.all_checks: dict[str, type] = {
            "line_length": type(LineLength),
            "replacement_characters": type(ReplacementCharacters),
            "tabs": type(Tabs),
            "todo": type(TODO),
            "trailing_whitespace": type(TrailingWhitespace),
            "region_newline": type(RegionNewline),
        }
        
    def generate_checks(self, configured_checks: dict[str, object]) -> list[Check]:
        checks = []
        for check_name, check_settings in configured_checks.items():
            checks.append(self.__create_check(check_name, check_settings))
        return checks
    
    def __create_check(self, wanted_check_name: str, check_settings: object) -> Check:
        for check_name, type_definition in self.all_checks.items():
            if check_name == wanted_check_name:
                check_instance = type_definition(check_settings)
                if not isinstance(check_instance, type(Check)):
                    raise TypeError(f"The type defined for '{wanted_check_name}' is not an instance of the abstract "
                                    f"class 'Check'. Please use 'Check' as the base class when writing new checks!")
                return check_instance
        raise NotImplementedError(f"Check '{wanted_check_name}' is not implemented.")