import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from excel_stock_updater import get_nasdaq_market_activity_price

def test_url(driver, url, expected_price=None):
    """Test the function on a specific URL and expected price."""
    logging.info(f"Testing URL: {url}")
    try:
        price = get_nasdaq_market_activity_price(driver, url)
        logging.info(f"Successfully extracted price: {price}")
        
        if expected_price:
            if abs(price - expected_price) < 0.01:  # Allow for small rounding differences
                logging.info(f"✓ Test passed! Extracted price {price} matches expected price {expected_price}")
            else:
                logging.warning(f"✗ Test failed! Extracted price {price} does not match expected price {expected_price}")
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
    
    # Test URLs provided by the user
    test_urls = [
        {"url": "https://www.nasdaq.com/market-activity/stocks/cxbtf", "expected_price": 464.00},
        {"url": "https://www.nasdaq.com/market-activity/etf/bits", "expected_price": 67.62}
    ]
    
    # Set up Chrome driver with headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    driver = None
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        # Test each URL
        results = []
        for test_case in test_urls:
            url = test_case["url"]
            expected_price = test_case["expected_price"]
            
            # Run the test
            price = test_url(driver, url, expected_price)
            results.append({
                "url": url,
                "expected_price": expected_price,
                "actual_price": price,
                "passed": price is not None and abs(price - expected_price) < 0.01
            })
            
            # Save page source for debugging
            source_filename = f"nasdaq_page_{url.split('/')[-1]}.html"
            with open(source_filename, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            logging.info(f"Saved page source to {source_filename}")
            
            # Wait a bit between requests to be nice to the server
            time.sleep(2)
            
        # Print summary
        logging.info("\n----- TEST RESULTS SUMMARY -----")
        for result in results:
            status = "PASSED" if result["passed"] else "FAILED"
            logging.info(f"{status}: {result['url']} - Expected: {result['expected_price']}, Got: {result['actual_price']}")
        
    except Exception as e:
        logging.error(f"Error in test: {e}", exc_info=True)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main() 