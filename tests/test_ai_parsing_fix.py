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

def test_ai_parsing_fix():
    """Test the AI parsing fix with the problematic URL"""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # The problematic URL from the log
    test_url = "https://globalxetfs.eu/funds/bt0x/#documents"
    
    print(f"Testing AI parsing fix with URL: {test_url}")
    print("=" * 80)
    
    driver = setup_driver()
    
    try:
        # Test the enhanced AI fallback
        result = extract_outstanding_shares_with_ai_fallback(driver, test_url)
        
        print(f"Result: {result}")
        
        if "outstanding_shares" in result:
            print(f"✅ SUCCESS: Found outstanding shares: {result['outstanding_shares']}")
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_ai_parsing_fix() 