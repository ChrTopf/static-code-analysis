@echo off
setlocal enabledelayedexpansion

:: create version timestamp
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd.HHmm"') do set TIMESTAMP=%%i
set APP_NAME=Static-Code-Analysis-V%TIMESTAMP%

:: create new output directory
mkdir dist\V%TIMESTAMP%

:: build application
.venv\Scripts\pyinstaller.exe --onefile --noconsole --name "%APP_NAME%" --distpath ".\dist\V%TIMESTAMP%" .\src\main.py -y
if %errorlevel% NEQ 0 (
  echo Could not build python application.
  pause
  exit /b 1
)

:: copy README and assets
robocopy assets dist\V%TIMESTAMP%\assets
copy README.md dist\V%TIMESTAMP%
copy analysis_config.json5 dist\V%TIMESTAMP%

pause
