@echo off

call %~dp0venv\Scripts\activate

cd %~dp0

set TOKEN=

python main.py

pause