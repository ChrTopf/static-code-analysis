from abc import abstractmethod


class Themeable:
    def _replace_theme_variables(self, variables: dict[str, str], stylesheet: str):
        for key, value in variables.items():
            stylesheet = stylesheet.replace(key, value)
        return stylesheet
    
    @abstractmethod
    def apply_theme(self, theme_variables: dict[str, str]) -> None:
        pass