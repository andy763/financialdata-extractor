#!/usr/bin/env python3
"""
Final comprehensive test of the outstanding_shares_updater.py fix
"""

import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Add the src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def final_comprehensive_test():
    """Final test with ALL valour.com URLs to confirm the bug is fixed"""
    
    # Import the functions from outstanding_shares_updater
    from outstanding_shares_updater import (
        extract_outstanding_shares_with_ai_fallback,
        CUSTOM_EXTRACTORS_AVAILABLE,
        IMPROVED_EXTRACTORS_AVAILABLE
    )
    
    print("=" * 80)
    print("FINAL COMPREHENSIVE TEST - VALOUR.COM BUG FIX VERIFICATION")
    print(f"CUSTOM_EXTRACTORS_AVAILABLE: {CUSTOM_EXTRACTORS_AVAILABLE}")
    print(f"IMPROVED_EXTRACTORS_AVAILABLE: {IMPROVED_EXTRACTORS_AVAILABLE}")
    print("=" * 80)
    
    # All test URLs with expected results
    test_cases = [
        ("https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd", "120,000"),
        ("https://valour.com/en/products/valour-bitcoin-physical-staking", "90,000"),
        ("https://valour.com/en/products/valour-ethereum-physical-staking", "185,000"),
        ("https://valour.com/en/products/valour-internet-computer-physical-staking", "5,848,803"),
        ("https://valour.com/en/products/1valour-stoxx-bitcoin-suisse-digital-asset-blue-chip", "789,818")
    ]
    
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = None
    success_count = 0
    total_count = len(test_cases)
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        print("\nRunning tests...")
        print("-" * 80)
        
        for i, (url, expected) in enumerate(test_cases, 1):
            print(f"\n[{i}/{total_count}] Testing: {url}")
            print(f"Expected: {expected}")
            
            try:
                result = extract_outstanding_shares_with_ai_fallback(driver, url)
                if result and 'outstanding_shares' in result:
                    actual = result['outstanding_shares']
                    method = result.get('method', 'unknown')
                    
                    print(f"Actual: {actual} (method: {method})")
                    
                    # Check if result matches expected
                    if actual == expected:
                        print("✅ PASS - Correct value returned")
                        success_count += 1
                    else:
                        print(f"❌ FAIL - Expected {expected}, got {actual}")
                else:
                    print("❌ FAIL - No result returned")
                    
            except Exception as e:
                print(f"❌ ERROR - {e}")
            
            print("-" * 40)
        
        # Final summary
        print("\n" + "=" * 80)
        print("FINAL TEST RESULTS")
        print("=" * 80)
        print(f"Successful tests: {success_count}/{total_count}")
        print(f"Success rate: {(success_count/total_count)*100:.1f}%")
        
        if success_count == total_count:
            print("🎉 ALL TESTS PASSED! The valour.com bug is FIXED!")
            print("✅ No more incorrect 120000 values for all URLs")
            print("✅ Each URL returns its correct outstanding shares value")
        else:
            print("⚠️ Some tests failed. The bug may not be fully fixed.")
            
        print("=" * 80)
            
    except Exception as e:
        print(f"Setup error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    final_comprehensive_test()
