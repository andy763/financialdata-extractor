import logging
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from excel_stock_updater import get_nasdaq_european_market_price

def main():
    # Configure logging to show debug messages
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Example URL from the user
    test_url = "https://www.nasdaq.com/european-market-activity/etn-etc/virbtce?id=HEX380452"
    
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
        
        # Test the function
        logging.info(f"Testing URL: {test_url}")
        
        # First, load the page ourselves to save the HTML for debugging
        driver.get(test_url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(5)
        
        # Save page source to a file for inspection
        page_source = driver.page_source
        with open("nasdaq_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        logging.info(f"Saved page source to nasdaq_page_source.html")
        
        # Print some basic page info
        logging.info(f"Page title: {driver.title}")
        
        # Look for price-related text in the page
        price_keywords = ["EUR", "USD", "GBP", "price", "Price", "value", "Value"]
        for keyword in price_keywords:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]")
            if elements:
                logging.info(f"Found {len(elements)} elements containing '{keyword}'")
                for i, element in enumerate(elements[:3]):  # Show first 3 elements only
                    logging.info(f"  {i+1}. {element.tag_name}: {element.text[:100]}...")
        
        # Now test our function
        price = get_nasdaq_european_market_price(driver, test_url)
        logging.info(f"Successfully extracted price: {price}")
        
        # Check if the price matches the expected value
        expected_price = 16.29
        if abs(price - expected_price) < 0.01:  # Allow for small rounding differences
            logging.info(f"✓ Test passed! Extracted price {price} matches expected price {expected_price}")
        else:
            logging.warning(f"✗ Test failed! Extracted price {price} does not match expected price {expected_price}")
            
    except Exception as e:
        logging.error(f"Error in test: {e}", exc_info=True)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main() 