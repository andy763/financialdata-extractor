#!/usr/bin/env python3
"""
Test integration of 1-error website functions in the main script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import fetch_and_extract_data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import logging

def test_1_error_integration():
    """Test the integrated 1-error website fixes in the main script"""
    
    # URLs to test (1-error websites)
    test_urls = [
        ("https://valour.com/en/products/valour-ethereum-physical-staking", "Valour"),
        ("https://www.nasdaq.com/european-market-activity/etn-etc/viralt?id=SSE366514", "NASDAQ European"),
        ("https://www.purposeinvest.com/funds/purpose-ether-staking-corp-etf", "Purpose Investments"),
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
        
        print("🎯 Testing 1-error website integration in main script:")
        print("=" * 80)
        
        for url, name in test_urls:
            print(f"\n🌐 Testing {name}: {url}")
            try:
                result = fetch_and_extract_data(driver, url, [])
                
                if "closing price" in result:
                    price = result["closing price"]
                    print(f"  ✅ SUCCESS: Found closing price {price}")
                    
                    # Check if it's a reasonable value
                    if isinstance(price, (int, float)) and 0.01 <= price <= 10000:
                        print(f"  🎉 EXCELLENT: Reasonable price value!")
                    else:
                        print(f"  ⚠️  WARNING: Price seems unusual")
                        
                elif "ai extracted price" in result:
                    price = result["ai extracted price"]
                    print(f"  ✅ SUCCESS (AI): Found AI extracted price {price}")
                    
                elif "error" in result:
                    print(f"  ❌ ERROR: {result['error']}")
                    
                else:
                    print(f"  ⚠️  UNEXPECTED: {result}")
                    
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                
    except Exception as e:
        print(f"Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_1_error_integration() 