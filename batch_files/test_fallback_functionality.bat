@echo off
echo Testing fallback URL functionality...

REM Modify the Python script to run the test_fallback_urls function
python -c "import outstanding_shares_updater; outstanding_shares_updater.test_fallback_urls()"
 
echo.
echo Test completed. Press any key to exit.
pause 