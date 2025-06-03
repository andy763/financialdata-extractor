#!/usr/bin/env python3
"""
Compare the first URL result between standalone test and updater test
"""

import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_valour_shares

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compare_first_url():
    """Compare the result for the first URL that still shows 120,000"""
    
    url = "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd"
    
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
        
        print(f"Testing URL: {url}")
        
        # Test with direct valour extractor
        result = extract_valour_shares(driver, url)
        print(f"Direct valour extractor result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    compare_first_url()
