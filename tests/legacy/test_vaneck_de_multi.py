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
from src.improved_custom_domain_extractors import extract_vaneck_de_shares

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_test():
    """
    Test our updated VanEck DE extractor with multiple URLs
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
        
        # Test URLs - different crypto ETPs from VanEck German site
        test_urls = [
            # Our main test URL - Avalanche ETP
            {
                "url": "https://www.vaneck.com/de/en/investments/avalanche-etp/overview/",
                "expected": "5853000"
            },
            # Bitcoin ETP
            {
                "url": "https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/",
                "expected": "28880000"
            },
            # Ethereum ETP
            {
                "url": "https://www.vaneck.com/de/en/investments/ethereum-etp/overview/",
                "expected": "14443000"
            },
            # Non-crypto product (should return None)
            {
                "url": "https://www.vaneck.com/de/en/investments/global-real-estate-ucits-etf/overview/",
                "expected": None
            }
        ]
        
        # Track test results
        success_count = 0
        failure_count = 0
        
        # Test each URL
        for test_case in test_urls:
            url = test_case["url"]
            expected = test_case["expected"]
            
            print(f"\n----- Testing URL: {url} -----")
            
            try:
                # Test the direct function
                logging.info(f"Testing VanEck DE extractor on: {url}")
                result = extract_vaneck_de_shares(driver, url)
                logging.info(f"Result: {result}")
                
                # Print the results
                print(f"URL: {url}")
                print(f"Result: {result or 'No result'}")
                print(f"Expected: {expected or 'No result'}")
                
                # Check if the result matches the expected value
                if result == expected:
                    success_count += 1
                    print(f"✅ SUCCESS - Got expected value: {result}")
                else:
                    failure_count += 1
                    print(f"❌ FAILURE - Expected: {expected}, Got: {result}")
                
            except Exception as e:
                logging.error(f"Error testing {url}: {e}")
                print(f"❌ Error: {e}")
                failure_count += 1
        
        # Print summary
        print("\n----- TEST SUMMARY -----")
        print(f"Total tests: {len(test_urls)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failure_count}")
        print(f"Success rate: {success_count/len(test_urls)*100:.1f}%")
        
    except Exception as e:
        logging.error(f"Test error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_test() 