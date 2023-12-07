@echo off
python --version 3>NUL
if errorlevel 1 goto errorNoPython

if exist gapalienv\ (
    rmdir /s /q gapalienv
)
python -m venv gapalienv
gapalienv\Scripts\pip.exe install -r requirements.txt

goto:eof

:errorNoPython
echo.
echo Error^: Python not installed
"C:\Program Files\used\systems\innoventiq\accumanager\required\excutables\python-3.7.3-amd64.exe"
