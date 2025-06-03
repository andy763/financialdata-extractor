import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import load_workbook, Workbook
from src.custom_domain_extractors import extract_with_custom_function

def test_specific_row():
    """
    Test script to verify the fallback URL functionality for a specific row
    that has a valour.com primary URL and a TradingView fallback URL.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("Testing specific row with valour.com and TradingView URLs...")
    
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
    test_filename = "test_specific_row.xlsx"
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
        # Test primary URL (valour.com)
        print("\nTesting primary URL (valour.com):")
        primary_url = test_ws['P2'].value
        print(f"Primary URL: {primary_url}")
        
        primary_result = extract_with_custom_function(driver, primary_url)
        print(f"Primary URL result: {primary_result}")
        
        # Test fallback URL (TradingView)
        print("\nTesting fallback URL (TradingView):")
        fallback_url = test_ws['Q2'].value
        print(f"Fallback URL: {fallback_url}")
        
        fallback_result = extract_with_custom_function(driver, fallback_url)
        print(f"Fallback URL result: {fallback_result}")
        
        # Verify results
        if "outstanding_shares" in primary_result:
            print("\n✅ Primary URL succeeded - valour.com extractor is working")
            print(f"   Shares: {primary_result['outstanding_shares']}")
        else:
            print("\n❌ Primary URL failed - valour.com extractor has issues")
            print(f"   Error: {primary_result.get('error', 'Unknown error')}")
            
        if "outstanding_shares" in fallback_result:
            print("\n✅ Fallback URL succeeded - TradingView extractor is working")
            print(f"   Shares: {fallback_result['outstanding_shares']}")
            if "note" in fallback_result:
                print(f"   Note: {fallback_result['note']}")
        else:
            print("\n❌ Fallback URL failed - TradingView extractor has issues")
            print(f"   Error: {fallback_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_specific_row() 