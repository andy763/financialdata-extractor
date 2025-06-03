#!/usr/bin/env python3
"""
Test script to verify the specific fixes for the three failing test cases
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Import the custom extractors
from src.custom_domain_extractors import extract_grayscale_shares, extract_vaneck_shares, extract_vaneck_de_shares

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Setup Chrome driver with options"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def test_specific_fixes():
    """Test the three specific fixes"""
    print("🧪 TESTING SPECIFIC EXTRACTOR FIXES")
    print("=" * 60)
    
    # Test cases with expected results
    test_cases = [
        {
            'name': 'Grayscale Bitcoin Cash Trust',
            'url': 'https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust',
            'expected': '47,123,300',
            'extractor': extract_grayscale_shares
        },
        {
            'name': 'VanEck US Bitcoin ETF HODL',
            'url': 'https://www.vaneck.com/us/en/investments/bitcoin-etf-hodl/literature/',
            'expected': '53,075,000',
            'extractor': extract_vaneck_shares
        },
        {
            'name': 'VanEck DE Polygon ETP',
            'url': 'https://www.vaneck.com/de/en/investments/polygon-etp/overview/',
            'expected': '1,561,000',
            'extractor': extract_vaneck_de_shares
        }
    ]
    
    driver = setup_driver()
    results = []
    
    try:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}: {test_case['name']}")
            print(f"URL: {test_case['url']}")
            print(f"Expected: {test_case['expected']}")
            
            try:
                # Call the extractor
                result = test_case['extractor'](driver, test_case['url'])
                
                if 'outstanding_shares' in result:
                    extracted = result['outstanding_shares']
                    success = extracted == test_case['expected']
                    
                    if success:
                        print(f"✅ SUCCESS: Extracted {extracted}")
                        status = "PASS"
                    else:
                        print(f"❌ MISMATCH: Extracted {extracted}, expected {test_case['expected']}")
                        status = "FAIL"
                else:
                    print(f"❌ ERROR: {result.get('error', 'Unknown error')}")
                    extracted = None
                    status = "ERROR"
                
                results.append({
                    'name': test_case['name'],
                    'expected': test_case['expected'],
                    'extracted': extracted,
                    'status': status
                })
                
            except Exception as e:
                print(f"❌ EXCEPTION: {e}")
                results.append({
                    'name': test_case['name'],
                    'expected': test_case['expected'],
                    'extracted': None,
                    'status': "EXCEPTION"
                })
            
            print("-" * 60)
    
    finally:
        driver.quit()
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    total = len(results)
    
    for result in results:
        status_emoji = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{status_emoji} {result['name']}: {result['status']}")
        if result['extracted']:
            print(f"   Expected: {result['expected']}")
            print(f"   Extracted: {result['extracted']}")
    
    print(f"\n🎯 RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All fixes working correctly!")
        return True
    else:
        print("⚠️  Some fixes still need attention")
        return False

if __name__ == "__main__":
    success = test_specific_fixes()
    exit(0 if success else 1)
