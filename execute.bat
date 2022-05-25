@echo off
set scripts= "%~dp0\scripts\run.py"
rem set scripts= "C:\app_trigger\scripts\run.py"
set venv= "%~dp0\venv\Scripts"
rem set venv= "C:\app_trigger\venv\Scripts"
set codes="%1"

call %venv%\activate.bat
%venv%\python.exe %scripts% %codes%
call %venv%\deactivate.bat
@echo on
