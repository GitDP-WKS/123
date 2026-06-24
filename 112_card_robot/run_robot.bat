@echo off
chcp 65001 > nul
call .venv\Scripts\activate
python -m src.robot
pause
