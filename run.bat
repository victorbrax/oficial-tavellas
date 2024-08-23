@echo off
cd venv\Scripts
call activate
SET FLASK_ENV=production
cd ..\..
python run.py
