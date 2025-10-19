import traceback

from gui.main_view import MainView


class Logger:
    def __init__(self, quiet: bool):
        self.view = None
        self.quiet = quiet
        
    def set_gui(self, view : MainView):
        self.view = view
        
    def __has_gui(self):
        return self.view is not None

    def debug(self, message : str):
        if not self.quiet:
            return
        print(f"[\033[35mDEBG\033[0m]: {message}")
        if self.__has_gui():
            self.view.log(message, level="DEBUG")

    def info(self, message : str):
        if not self.quiet:
            return
        print(f"[\033[32mINFO\033[0m]: {message}")
        if self.__has_gui():
            self.view.log(message, "INFO")

    def warn(self, message : str):
        print(f"[\033[33mWARN\033[0m]: {message}")
        if self.__has_gui():
            self.view.log(message, "WARNING")

    def error(self, message : str | Exception):
        if isinstance(message, Exception):
            print(f"\033[31m[FATA]: {traceback.format_exc()}\033[0m")
            if self.__has_gui():
                self.view.log(message, "ERROR")
        else:
            print(f"\033[31m[FATA]: {message}\033[0m")
            if self.__has_gui():
                self.view.log(message, "ERROR")