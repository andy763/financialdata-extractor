#!/usr/bin/env python3
"""
Test the outstanding_shares_updater.py with valour.com URLs to check if it returns 120000
"""

import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Add the src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_valour_with_outstanding_shares_updater():
    """Test valour.com URLs using the actual outstanding_shares_updater.py logic"""
      # Import the functions from outstanding_shares_updater
    from outstanding_shares_updater import (
        extract_outstanding_shares_with_ai_fallback,
        extract_with_custom_function,
        CUSTOM_EXTRACTORS_AVAILABLE,
        IMPROVED_EXTRACTORS_AVAILABLE
    )
    
    print("=" * 80)
    print("TESTING VALOUR.COM WITH OUTSTANDING_SHARES_UPDATER.PY")
    print(f"CUSTOM_EXTRACTORS_AVAILABLE: {CUSTOM_EXTRACTORS_AVAILABLE}")
    print(f"IMPROVED_EXTRACTORS_AVAILABLE: {IMPROVED_EXTRACTORS_AVAILABLE}")
    print("=" * 80)
    
    # Test URLs
    test_urls = [
        "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd",
        "https://valour.com/en/products/valour-bitcoin-physical-staking",
        "https://valour.com/en/products/valour-ethereum-physical-staking"
    ]
    
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        for url in test_urls:
            print(f"\nTesting URL: {url}")
            
            # Test with custom function directly
            if extract_with_custom_function:
                try:
                    custom_result = extract_with_custom_function(driver, url)
                    print(f"Custom function result: {custom_result}")
                except Exception as e:
                    print(f"Custom function error: {e}")
              # Test with the main extraction function
            try:
                result = extract_outstanding_shares_with_ai_fallback(driver, url)
                print(f"Main extraction result: {result}")
                
                # Check if it's returning 120000 (the bug)
                if result and "120000" in str(result):
                    print("🚨 BUG DETECTED: Returned 120000!")
                elif result and "120,000" in str(result):
                    print("🚨 BUG DETECTED: Returned 120,000!")
                else:
                    print("✅ Result looks good")
                    
            except Exception as e:
                print(f"Main extraction error: {e}")
            
            print("-" * 40)
            
    except Exception as e:
        print(f"Setup error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_valour_with_outstanding_shares_updater()
