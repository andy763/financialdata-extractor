import sys
import os
import logging
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the function we want to test
from src.improved_custom_domain_extractors import extract_vaneck_de_shares, extract_with_custom_function

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_test():
    """
    Test our updated VanEck DE extractor
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        # Test URL - VanEck German site with Avalanche ETP
        test_url = "https://www.vaneck.com/de/en/investments/avalanche-etp/overview/"
        
        # Test the direct function
        logging.info(f"Testing VanEck DE extractor directly on: {test_url}")
        result_direct = extract_vaneck_de_shares(driver, test_url)
        logging.info(f"Direct function result: {result_direct}")
        
        # Test the extract_with_custom_function which should detect vaneck.com/de
        logging.info(f"Testing custom function extractor on: {test_url}")
        result_custom = extract_with_custom_function(driver, test_url)
        logging.info(f"Custom function result: {result_custom}")
        
        # Print the results
        print("\n----- TEST RESULTS -----")
        print(f"URL: {test_url}")
        print(f"Direct VanEck DE extractor: {result_direct or 'No result'}")
        print(f"extract_with_custom_function: {result_custom or 'No result'}")
        print("Expected value: 5,853,000")
        print("-----------------------\n")
        
        if result_direct == "5853000":
            print("✅ Direct extractor works correctly!")
        else:
            print("❌ Direct extractor failed or returned incorrect value")
            
        if result_custom == "5853000":
            print("✅ extract_with_custom_function works correctly!")
        else:
            print("❌ extract_with_custom_function failed or returned incorrect value")
        
    except Exception as e:
        logging.error(f"Test error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_test() 