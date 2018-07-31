@echo off
set scripts= "D:\daguado\dev_tools\app_trigger\scripts\run.py"
set venv= "D:\daguado\dev_tools\app_trigger\venv\Scripts"
set codes="%1"

call %venv%\activate.bat
%venv%\python.exe %scripts% %codes%
call %venv%\deactivate.bat
@echo on
