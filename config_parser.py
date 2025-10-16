import json
import os.path

import json5

from analysis_config import AnalysisConfig
from models.analysis_arguments import AnalysisArguments


class ConfigParser:
    
    def __init__(self):
        self.analysis_arguments_file_path = "analysis_arguments.json"
    
    #region analysis_config
    
    def load_analysis_config(self, file_path: str) -> AnalysisConfig:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_root = json5.load(file)
            return self.__parse_analysis_config(json_root)

    def __parse_analysis_config(self, json_root: dict[str, object]) -> AnalysisConfig:
        forbidden_files = self.__parse_file_wildcard_list(json_root, 'forbidden_files')
        ignored_files = self.__parse_file_wildcard_list(json_root, 'ignored_files')
        file_encodings = self.__parse_file_encodings(json_root)
        standard_checks = self.__parse_standard_checks(json_root)
        specific_checks = self.__parse_specific_checks(json_root)
        return AnalysisConfig(forbidden_files, ignored_files, file_encodings, standard_checks, specific_checks)
    
    def __parse_file_wildcard_list(self, json_root: dict[str, object], property_name: str) -> list[str]:
        file_wildcards = json_root.get(property_name, [])
        if not isinstance(file_wildcards, list):
            raise ValueError(f"The property '{property_name}' must be a list.")
        for item in file_wildcards:
            if not isinstance(item, str):
                raise ValueError(f"Every entry in '{property_name}' must be a string.")
        return [str(item) for item in file_wildcards]
    
    def __parse_file_encodings(self, json_root: dict[str, object]) -> dict[str, str]:
        file_encodings = json_root.get('file_encodings', {})
        if not isinstance(file_encodings, dict):
            raise ValueError("The property 'file_encodings' must be an object.")
        for key, value in file_encodings.items():
            if not isinstance(value, str):
                raise ValueError("Every value in 'file_encodings' must be a string.")
        return file_encodings
    
    def __parse_standard_checks(self, json_root: dict[str, object]) -> dict[str, object]:
        standard_checks = json_root.get('standard_checks', {})
        if not isinstance(standard_checks, dict):
            raise ValueError("The property 'standard_checks' must be an object.")
        return standard_checks
    
    def __parse_specific_checks(self, json_root: dict[str, object]) -> dict[str, dict[str, object]]:
        specific_checks = json_root.get('specific_checks', {})
        if not isinstance(specific_checks, dict):
            raise ValueError("The property 'specific_checks' must be an object.")
        for key, value in specific_checks.items():
            if not isinstance(value, dict):
                raise ValueError("Every value in 'specific_checks' must be an object.")
        return specific_checks
       
    #endregion analysis_config
    
    #region analysis_arguments
    
    def load_analysis_arguments(self) -> AnalysisArguments:
        if self.__file_exists(self.analysis_arguments_file_path):
            return self.__load_analysis_arguments_from_file(self.analysis_arguments_file_path)
        else:
            return AnalysisArguments("", "", "", True)
    
    def __file_exists(self, file_path: str) -> bool:
        return os.path.isfile(file_path)
    
    def __load_analysis_arguments_from_file(self, file_name: str) -> AnalysisArguments:
        with open(file_name, 'r', encoding='utf-8') as file:
            json_root = json.load(file)
            repository_directory = self.__load_property_from_json_object(
                json_root, 
                "repository_directory", 
                type(str))
            source_branch = self.__load_property_from_json_object(
                json_root,
                "source_branch",
                type(str)
            )
            destination_branch = self.__load_property_from_json_object(
                json_root,
                "destination_branch",
                type(str)
            )
            changed_lines_only = self.__load_property_from_json_object(
                json_root,
                "changed_lines_only",
                type(bool)
            )
            return AnalysisArguments(repository_directory, source_branch, destination_branch, changed_lines_only)
    
    def store_analysis_arguments(self, analysis_arguments: AnalysisArguments):
        with open(self.analysis_arguments_file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(analysis_arguments))
    
    #endregion analysis_arguments
    
    def __load_property_from_json_object(self, 
                                         json_object: dict[str, object], 
                                         property_name: str, 
                                         property_type: type) -> object:
        if not isinstance(json_object, dict):
            raise ValueError("The root element of the json data must be an object.")
        property_value = json_object.get(property_name, None)
        if not isinstance(property_value, property_type):
            raise ValueError(f"The property '{property_name}' must be a string.")
        return property_value