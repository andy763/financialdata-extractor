@echo off
echo ===============================================
echo    Stock and Shares Outstanding Data Extractor
echo ===============================================
echo.
echo Starting stock price extraction...
python excel_stock_updater.py
echo.
echo Starting outstanding shares extraction...
python outstanding_shares_updater.py
echo.
echo ===============================================
echo All data extraction completed!
echo Results saved to: data/Custodians_Results.xlsx
echo ===============================================
pause 