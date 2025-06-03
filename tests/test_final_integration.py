#!/usr/bin/env python3
"""
Final integration test for BetaShares and CSO P Asset fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import fetch_and_extract_data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import logging

def test_final_integration():
    """Test the final integrated fixes for BetaShares and CSO P Asset"""
    
    # URLs to test
    test_urls = [
        ("https://www.betashares.com.au/fund/crypto-innovators-etf/#resources", "BetaShares"),
        ("https://www.csopasset.com/en/products/hk-btcfut#", "CSO P Asset"),
    ]
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        
        print("🎯 FINAL INTEGRATION TEST - Testing fixes in main script")
        print("=" * 80)
        
        for url, name in test_urls:
            print(f"\n🌐 Testing {name}: {url}")
            try:
                # Use the main script's fetch_and_extract_data function
                result = fetch_and_extract_data(driver, url, [])
                
                if "error" in result:
                    print(f"  ❌ FAILED: {result}")
                else:
                    # Extract the price value from the result
                    price_key = list(result.keys())[0]
                    price_value = result[price_key]
                    print(f"  ✅ SUCCESS: {price_key} = ${price_value}")
                    
                    # Check if it's a .0 value
                    if isinstance(price_value, (int, float)) and price_value == int(price_value):
                        print(f"  ⚠️  WARNING: Still a .0 value, but may be correct")
                    else:
                        print(f"  🎉 EXCELLENT: Non-.0 value with proper decimals!")
                        
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                
    except Exception as e:
        print(f"Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_final_integration() 