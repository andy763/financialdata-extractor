@echo off
echo Ensuring we are in the script's directory...
cd /d "%~dp0"

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Running the Python script (excel_stock_updater.py)...
python excel_stock_updater.py

echo.
echo Script execution finished.
echo Press any key to close this window.
pause >nul 