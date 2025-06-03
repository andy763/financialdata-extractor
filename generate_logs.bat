@echo off
echo Stock Prices and Outstanding Shares Log Generator
echo ================================================

if "%1"=="" (
    echo Please specify a log type:
    echo   stock    - Generate stock prices log
    echo   shares   - Generate outstanding shares log 
    echo   combined - Generate both logs and combine them
    exit /b
)

if "%2"=="" (
    set excel_file=custodians.xlsx
) else (
    set excel_file=%2
)

echo Generating %1 log from %excel_file%...
python src/generate_logs.py %1 %excel_file%

echo.
echo Done! 