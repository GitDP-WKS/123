@echo off
chcp 65001 > nul

python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium

echo.
echo Установка завершена.
echo Скопируйте config.example.json в config.json и заполните настройки.
pause
