#!/usr/bin/env python3
"""
Test the integrated .0 fixes in the main script
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Add the current directory to the path so we can import from excel_stock_updater
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import fetch_and_extract_data

def test_integrated_fixes():
    """Test the integrated .0 fixes in the main script"""
    
    # URLs that had .0 errors and should now be fixed
    test_urls = [
        ("https://www.schwabassetmanagement.com/products/stce", "Schwab Asset Management"),
        ("https://evolveetfs.com/product/ethr#tab-content-overview/", "Evolve ETFs"),
        ("https://www.21shares.com/en-us/product/arkb", "21Shares"),
        ("https://www.ninepoint.com/funds/ninepoint-crypto-and-ai-leaders-etf/", "Ninepoint"),
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
        
        print("🧪 Testing integrated .0 fixes in main script:")
        print("=" * 80)
        
        for url, name in test_urls:
            print(f"\n🌐 Testing {name}: {url}")
            try:
                # Use the main fetch_and_extract_data function
                result = fetch_and_extract_data(driver, url, [])
                
                if isinstance(result, dict):
                    # Check if we got a valid price (not an error)
                    price_keys = [k for k in result.keys() if 'price' in k.lower() and 'error' not in k.lower()]
                    if price_keys:
                        price_key = price_keys[0]
                        price_value = result[price_key]
                        
                        # Check if it's a valid non-.0 price
                        if isinstance(price_value, (int, float)):
                            if price_value != int(price_value):  # Has decimals
                                print(f"  ✅ SUCCESS: Found {price_key}: ${price_value}")
                            else:
                                print(f"  ⚠️  WARNING: Still .0 value - {price_key}: ${price_value}")
                        else:
                            print(f"  ❌ FAILED: Non-numeric result - {price_key}: {price_value}")
                    else:
                        # Check for errors
                        error_keys = [k for k in result.keys() if 'error' in k.lower()]
                        if error_keys:
                            print(f"  ❌ FAILED: {result[error_keys[0]]}")
                        else:
                            print(f"  ❌ FAILED: No price found - {result}")
                else:
                    print(f"  ❌ FAILED: Unexpected result type - {result}")
                    
            except Exception as e:
                print(f"  ❌ FAILED: Exception - {e}")
                
    except Exception as e:
        print(f"Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_integrated_fixes() 