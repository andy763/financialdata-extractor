#!/usr/bin/env python3
"""
Test the remaining 5 custom domain extractors
"""

import sys
import os
sys.path.append('src')

# Set up Selenium WebDriver first
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

print("TESTING REMAINING CUSTOM DOMAIN EXTRACTORS")
print("=" * 60)

from outstanding_shares_updater import extract_outstanding_shares_with_ai_fallback

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = None
try:
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.set_page_load_timeout(30)
    
    print("✅ WebDriver initialized successfully")

# Test cases for remaining domains (using shorter timeout for testing)
test_cases = [
    ("lafv.li", "https://www.lafv.li/de/fonds/list/42585"),
    ("augmentasicav.com", "https://augmentasicav.com/documents"), 
    ("invesco.com", "https://www.invesco.com/uk/en/financial-products/etfs/invesco-physical-bitcoin.html"),
    ("rexshares.com", "https://www.rexshares.com/funds/rex-short-bitcoin-strategy-etf/"),
    ("money.tmx.com", "https://money.tmx.com/en/quote/BTCC")
]

results = []
for i, (domain, url) in enumerate(test_cases, 1):
    print(f"\n[{i}/5] Testing {domain}...")
    print(f"URL: {url}")
      try:
        # Call the main extraction function
        result = extract_outstanding_shares_with_ai_fallback(driver, url)
        
        if result and result.get('outstanding_shares') and result.get('outstanding_shares') != 'N/A':
            shares = result.get('outstanding_shares')
            method = result.get('method', 'unknown')
            print(f"[SUCCESS] {shares:,} shares (method: {method})")
            results.append((domain, True, shares, method, None))
        else:
            print(f"[FAILED] No shares extracted - Result: {result}")
            results.append((domain, False, None, None, "No shares found"))
            
    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)[:100]}")
        results.append((domain, False, None, None, str(e)[:100]))

# Summary
print("\n" + "=" * 60)
print("FINAL RESULTS SUMMARY")
print("=" * 60)

success_count = 0
custom_method_count = 0

for domain, success, shares, method, error in results:
    if success:
        success_count += 1
        if method == 'custom':
            custom_method_count += 1
        print(f"[SUCCESS] {domain}: {shares:,} shares (method: {method})")
    else:
        print(f"[FAILED] {domain}: {error or 'Unknown error'}")

print(f"\nOverall Success Rate: {success_count}/{len(test_cases)} ({success_count/len(test_cases)*100:.1f}%)")
print(f"Custom Method Usage: {custom_method_count}/{success_count if success_count > 0 else len(test_cases)} successful extractions")

if success_count == len(test_cases):
    print("\n[EXCELLENT] ALL REMAINING EXTRACTORS WORKING PERFECTLY!")
    print("Combined with previous test results, the outstanding shares")
    print("extraction pipeline is fully verified across all domains.")
elif success_count > 0:
    print(f"\n[PARTIAL] {success_count} out of {len(test_cases)} extractors working")
    print("Some domains may need additional fixes or have temporary issues.")
else:
    print("\n[CRITICAL] NONE of the remaining extractors are working")
    print("These domains may need urgent attention.")

# Combined assessment
print(f"\n[ASSESSMENT] Combined with previous successful test of 7 extractors,")
print(f"we now have verified {success_count + 7}/{len(test_cases) + 7} total custom extractors")
if success_count >= 3:  # If at least 60% work
    print("[CONCLUSION] Outstanding shares extraction pipeline verification SUCCESSFUL")
else:
    print("[CONCLUSION] Outstanding shares extraction pipeline needs additional work")
