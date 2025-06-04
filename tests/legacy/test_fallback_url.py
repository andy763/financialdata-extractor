import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from src.custom_domain_extractors import extract_with_custom_function

def test_fallback_url():
    """
    Test script to verify the fallback URL functionality specifically for TradingView URLs.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("Testing TradingView URL handling...")
    
    # Create a test workbook
    test_wb = Workbook()
    test_ws = test_wb.active
    test_ws.title = "Test"
    
    # Add headers
    test_ws['P1'] = "Primary URL"
    test_ws['Q1'] = "Fallback URL"
    test_ws['M1'] = "Outstanding Shares"
    
    # Test case: TradingView URL with FWB-CH pattern
    test_ws['P2'] = "https://valour.com/digital-assets/bitcoin"  # This should fail
    test_ws['Q2'] = "https://www.tradingview.com/symbols/FWB-CH114913970/"  # This should work
    
    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # Test primary URL
        print("\nTesting primary URL (should fail):")
        primary_url = test_ws['P2'].value
        print(f"Primary URL: {primary_url}")
        
        primary_result = extract_with_custom_function(driver, primary_url)
        print(f"Primary URL result: {primary_result}")
        
        # Test fallback URL
        print("\nTesting fallback URL (should succeed):")
        fallback_url = test_ws['Q2'].value
        print(f"Fallback URL: {fallback_url}")
        
        fallback_result = extract_with_custom_function(driver, fallback_url)
        print(f"Fallback URL result: {fallback_result}")
        
        # Verify results
        if "error" in primary_result and "outstanding_shares" in fallback_result:
            print("\n✅ TEST PASSED: Primary URL failed and fallback URL succeeded as expected")
        else:
            print("\n❌ TEST FAILED: Unexpected results")
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_fallback_url() 