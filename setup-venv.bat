@echo off
"C:\Program Files\Python313\python.exe" -m venv .venv
.venv\Scripts\pip.exe install PyQt5
.venv\Scripts\pip.exe install easygui
.venv\Scripts\pip.exe install pytz
.venv\Scripts\pip.exe install pyinstaller
.venv\Scripts\pip.exe install GitPython
.venv\Scripts\pip.exe install PathSpec
.venv\Scripts\pip.exe install json5
pause