from abc import abstractmethod

from PyQt5.QtWidgets import QWidget


class ThemeableWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self._is_dark_mode = True
    
    @abstractmethod
    def get_stylesheet(self) -> str:
        pass        
    
    def apply_theme(self, is_dark_mode: bool) -> None:
        self._is_dark_mode = is_dark_mode
        if is_dark_mode:
            theme_variables = self.__get_dark_theme_variables()
        else:
            theme_variables = self.__get_light_theme_variables()
        self.setStyleSheet(self.__replace_theme_variables(theme_variables, self.__build_stylesheet()))
        self.__apply_theme_to_children(is_dark_mode)
        
    def repaint(self):
        self.apply_theme(self._is_dark_mode)
            
    def __build_stylesheet(self) -> str:
        return self.__get_default_stylesheet() + "\n" + self.get_stylesheet()

    def __replace_theme_variables(self, variables: dict[str, str], stylesheet: str):
        for key, value in variables.items():
            stylesheet = stylesheet.replace(key, value)
        return stylesheet
    
    def __apply_theme_to_children(self, is_dark_mode: bool):
        children = self.children()
        for child in self.children():
            if isinstance(child, ThemeableWidget):
                child.apply_theme(is_dark_mode)

    def __get_dark_theme_variables(self) -> dict[str, str]:
        return {
            "$primary": "#9e0000",
            "$secondary": "#884600",
            "$success": "#00c100",
            "$light": "#000000",
            "$dark": "#e1e1e1",
            "$body-bg-light": "#262626",
            "$body-bg-dark": "#101010",
            "$body-bg": "#1a1a1a"
        }

    def __get_light_theme_variables(self) -> dict[str, str]:
        return {
            "$primary": "#ea0000",
            "$secondary": "#ffa115",
            "$success": "#00c100",
            "$light": "#ffffff",
            "$dark": "#000000",
            "$body-bg-light": "#ffffff",
            "$body-bg-dark": "#e0e0e0",
            "$body-bg": "#fefefe"
        }

    def __get_default_stylesheet(self):
        return """            
            QCheckBox {
                color: $dark;
                font-weight: bold;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid $dark;
                border-radius: 3px;
                background-color: $body-bg-light;
            }
            
            QCheckBox::indicator:checked {
                background-color: $primary;
                border-color: $primary;
            }
            
            QCheckBox::indicator:checked:before {
                color: $dark;
                font-weight: bold;
            }
            
            QSplitter::handle {
                background-color: $body-bg;
                height: 3px;
            }
            
            QSplitter::handle:hover {
                background-color: $secondary;
            }
            
            QTabWidget::pane {
                border: 1px solid $body-bg-light;
                border-radius: 4px;
                background-color: $body-bg;
            }
            
            QTabBar::tab {
                background-color: $body-bg-light;
                color: $dark;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: $primary;
                color: $dark;
            }
            
            QTabBar::tab:hover {
                background-color: $secondary;
            }
        """