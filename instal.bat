:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython


:: Reaching here means Python is installed.
:: Execute stuff...
pip3 install -r requirements.txt

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed
"C:\Program Files\used\systems\innoventiq\accumanager\required\excutables\python-3.7.3-amd64.exe"
