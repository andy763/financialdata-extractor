import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from excel_stock_updater import get_nasdaq_european_market_price

def test_url(driver, url, expected_price=None, expected_currency=None):
    """Test the function on a specific URL and expected price."""
    logging.info(f"Testing URL: {url}")
    try:
        price = get_nasdaq_european_market_price(driver, url)
        logging.info(f"Successfully extracted price: {price}")
        
        if expected_price:
            # Allow for price changes within a reasonable range (±5%)
            price_min = expected_price * 0.95
            price_max = expected_price * 1.05
            if price_min <= price <= price_max:
                logging.info(f"✓ Test passed! Extracted price {price} is within ±5% of expected price {expected_price}")
            else:
                logging.warning(f"✗ Test failed! Extracted price {price} is outside ±5% range of expected price {expected_price}")
        return price
    except Exception as e:
        logging.error(f"Error in test for URL {url}: {e}", exc_info=True)
        return None

def main():
    # Configure logging to show debug messages
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test URLs with different currencies
    test_urls = [
        {
            "url": "https://www.nasdaq.com/european-market-activity/etn-etc/viralt?id=SSE366514",
            "expected_price": 15.78,
            "expected_currency": "SEK"
        },
        {
            "url": "https://www.nasdaq.com/european-market-activity/etn-etc/btce?id=XETR391789",
            "expected_price": 35.20,
            "expected_currency": "EUR"
        },
        {
            "url": "https://www.nasdaq.com/european-market-activity/etn-etc/virbtce?id=HEX380452",
            "expected_price": 35.20,
            "expected_currency": "EUR"
        }
    ]
    
    # Set up Chrome driver with headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        
        for test_case in test_urls:
            logging.info(f"\nTesting URL: {test_case['url']}")
            logging.info(f"Expected: {test_case['expected_currency']} {test_case['expected_price']}")
            
            try:
                price = test_url(driver, test_case['url'], test_case['expected_price'], test_case['expected_currency'])
                if price:
                    logging.info(f"✓ Successfully extracted price: {price}")
                else:
                    logging.error("✗ Failed to extract price")
            except Exception as e:
                logging.error(f"✗ Error testing URL: {e}")
                
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main() 