import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import load_workbook, Workbook
from src.custom_domain_extractors import extract_with_custom_function

# Mock the valour.com extractor to force it to fail
def mock_extract_with_custom_function(driver, url):
    """
    Mock function that forces valour.com URLs to fail but lets other extractors work normally
    """
    if "valour.com" in url.lower():
        print("Mocking valour.com extractor to fail")
        return {"error": "Forced failure for testing"}
    else:
        # Use the real extractor for other URLs
        from src.custom_domain_extractors import extract_with_custom_function as real_extract
        return real_extract(driver, url)

def test_fallback_behavior():
    """
    Test script to verify the fallback URL behavior by forcing the primary URL to fail
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("Testing fallback behavior with forced primary URL failure...")
    
    # Create a test workbook with the specific URLs
    test_wb = Workbook()
    test_ws = test_wb.active
    test_ws.title = "Test"
    
    # Add headers
    test_ws['P1'] = "Primary URL"
    test_ws['Q1'] = "Fallback URL"
    test_ws['M1'] = "Outstanding Shares"
    
    # Add the specific test case
    test_ws['P2'] = "https://valour.com/de/products/physical-bitcoin-carbon-neutral-eur"  # valour.com URL
    test_ws['Q2'] = "https://www.tradingview.com/symbols/FWB-CH114913970/"  # TradingView URL
    
    # Save the test file
    test_filename = "test_fallback_behavior.xlsx"
    test_wb.save(test_filename)
    print(f"Created test file: {test_filename}")
    
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
        # Test primary URL (valour.com) with forced failure
        print("\nTesting primary URL (valour.com) with forced failure:")
        primary_url = test_ws['P2'].value
        print(f"Primary URL: {primary_url}")
        
        primary_result = mock_extract_with_custom_function(driver, primary_url)
        print(f"Primary URL result: {primary_result}")
        
        # Test fallback URL (TradingView)
        print("\nTesting fallback URL (TradingView):")
        fallback_url = test_ws['Q2'].value
        print(f"Fallback URL: {fallback_url}")
        
        fallback_result = mock_extract_with_custom_function(driver, fallback_url)
        print(f"Fallback URL result: {fallback_result}")
        
        # Simulate the main function's fallback behavior
        print("\nSimulating main function fallback behavior:")
        if "error" in primary_result:
            print(f"Primary URL failed: {primary_result['error']}")
            print(f"Trying fallback URL: {fallback_url}")
            
            if "outstanding_shares" in fallback_result:
                print(f"✅ Fallback URL succeeded: {fallback_result['outstanding_shares']}")
                if "note" in fallback_result:
                    print(f"Note: {fallback_result['note']}")
            else:
                print(f"❌ Fallback URL failed: {fallback_result.get('error', 'Unknown error')}")
        else:
            print(f"Primary URL succeeded (no fallback needed): {primary_result['outstanding_shares']}")
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_fallback_behavior() 