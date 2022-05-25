@echo off
set scripts= "C:\app_trigger\scripts\runnew.py"
set venv= "C:\app_trigger\venv\Scripts"
set codes="%1"

call %venv%\activate.bat
rem %venv%\python.exe %scripts% %codes%
call %venv%\deactivate.bat
@echo on
