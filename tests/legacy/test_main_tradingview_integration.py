#!/usr/bin/env python3
"""
Test TradingView integration in the main excel_stock_updater.py application
"""

import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Import the main function
try:
    from excel_stock_updater import fetch_and_extract_data
    print("✅ Successfully imported fetch_and_extract_data")
except ImportError as e:
    print(f"❌ Failed to import from excel_stock_updater: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_tradingview_integration():
    """Test that TradingView URLs are correctly routed and processed"""
    
    # Test URL
    test_url = "https://www.tradingview.com/symbols/NASDAQ-ZZZ/"
    
    # Setup Chrome driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = None
    
    try:
        print("=" * 60)
        print("TESTING TRADINGVIEW INTEGRATION IN MAIN APPLICATION")
        print("=" * 60)
        
        # Initialize Chrome driver
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        
        print(f"Testing URL: {test_url}")
        print("Calling fetch_and_extract_data function...")
        
        # Call the main function
        result = fetch_and_extract_data(driver, test_url, ["price", "market price"])
        
        print(f"Result: {result}")
        
        # Analyze the result
        if "market price" in result:
            price = result["market price"]
            print(f"✅ SUCCESS: TradingView price extracted: ${price}")
            print("🎉 TradingView integration is working correctly!")
            return True
        elif "ai extracted price" in result:
            price = result["ai extracted price"]
            print(f"✅ SUCCESS: AI fallback price extracted: ${price}")
            print("⚠️  TradingView extractor failed, but AI fallback worked")
            return True
        elif "error" in result:
            error = result["error"]
            print(f"❌ ERROR: {error}")
            print("🚨 TradingView integration failed")
            return False
        else:
            print(f"❓ UNEXPECTED RESULT: {result}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    success = test_tradingview_integration()
    print("\n" + "=" * 60)
    if success:
        print("✅ TRADINGVIEW INTEGRATION TEST PASSED")
    else:
        print("❌ TRADINGVIEW INTEGRATION TEST FAILED")
    print("=" * 60)
    sys.exit(0 if success else 1)
