#!/usr/bin/env python3

import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from outstanding_shares_updater import extract_outstanding_shares_with_ai_fallback

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def test_comprehensive_ai_fix():
    """Test the AI parsing fix with multiple problematic URLs"""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test URLs that were previously problematic
    test_urls = [
        "https://globalxetfs.eu/funds/bt0x/#documents",  # The original problematic URL
        "https://valour.com/products/valour-bitcoin-physical-carbon-neutral-etp",  # Valour example
        "https://grayscale.com/products/grayscale-bitcoin-trust-btc/",  # Grayscale example
    ]
    
    print("Testing AI parsing fix with multiple URLs")
    print("=" * 80)
    
    driver = setup_driver()
    results = []
    
    try:
        for i, test_url in enumerate(test_urls, 1):
            print(f"\n{i}. Testing: {test_url}")
            print("-" * 60)
            
            try:
                # Test the enhanced AI fallback
                result = extract_outstanding_shares_with_ai_fallback(driver, test_url)
                
                if "outstanding_shares" in result:
                    print(f"✅ SUCCESS: Found outstanding shares: {result['outstanding_shares']}")
                    results.append({"url": test_url, "status": "success", "shares": result['outstanding_shares']})
                else:
                    print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                    results.append({"url": test_url, "status": "failed", "error": result.get('error', 'Unknown error')})
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                results.append({"url": test_url, "status": "error", "error": str(e)})
                
    finally:
        driver.quit()
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    total_count = len(results)
    
    print(f"Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        if result["status"] == "success":
            print(f"{status_icon} {result['url']}: {result['shares']}")
        else:
            print(f"{status_icon} {result['url']}: {result['error']}")

if __name__ == "__main__":
    test_comprehensive_ai_fix() 