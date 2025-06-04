#!/usr/bin/env python3
"""
Test the specific VanEck DE polygon-etp URL that was mentioned
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_vaneck_de_shares

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

def test_polygon_etp():
    """Test the specific polygon-etp URL"""
    print("🔍 TESTING SPECIFIC VanEck DE Polygon ETP URL")
    print("=" * 60)
    
    url = 'https://www.vaneck.com/de/en/investments/polygon-etp/overview/'
    expected = '1,561,000'
    
    print(f"URL: {url}")
    print(f"Expected: {expected}")
    
    driver = setup_driver()
    
    try:
        result = extract_vaneck_de_shares(driver, url)
        
        if 'outstanding_shares' in result:
            extracted = result['outstanding_shares']
            success = extracted == expected
            
            if success:
                print(f"✅ SUCCESS: Extracted {extracted}")
                return True
            else:
                print(f"❌ MISMATCH: Extracted {extracted}, expected {expected}")
                return False
        else:
            print(f"❌ ERROR: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    success = test_polygon_etp()
    exit(0 if success else 1)
