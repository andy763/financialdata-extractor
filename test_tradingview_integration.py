"""
Test TradingView Integration in Main Application
This script tests the TradingView price extraction function within the main excel_stock_updater.py
"""

import logging
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import fetch_and_extract_data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_tradingview_integration():
    """Test the TradingView integration in the main application"""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test URLs
    test_urls = [
        "https://www.tradingview.com/symbols/NASDAQ-ZZZ/",
        "https://www.tradingview.com/symbols/CBOE-ARKZ/"
    ]
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    try:
        for url in test_urls:
            logging.info(f"\n--- Testing TradingView Integration: {url} ---")
            try:
                # Test using the main application function
                result = fetch_and_extract_data(driver, url, keywords=["price"])
                
                if "market price" in result:
                    logging.info(f"SUCCESS: Main app extracted price {result['market price']} from {url}")
                elif "ai extracted price" in result:
                    logging.info(f"SUCCESS (AI Fallback): Main app extracted price {result['ai extracted price']} from {url}")
                elif "error" in result:
                    logging.error(f"FAILED: {result['error']} for {url}")
                else:
                    logging.error(f"UNEXPECTED RESULT: {result} for {url}")
                
            except Exception as e:
                logging.error(f"EXCEPTION: {e} for {url}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    test_tradingview_integration()
