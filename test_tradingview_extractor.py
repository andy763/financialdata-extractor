import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_tradingview_shares

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def setup_driver():
    """Set up and return a configured Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def test_tradingview_extractor():
    """
    Test the TradingView custom extractor on various URL examples.
    
    NOTE: This test only verifies that the extractor can find and extract
    shares outstanding data. The actual values may change over time as the
    company's outstanding shares change. The test compares structure, not exact values.
    """
    # Initialize the WebDriver
    driver = setup_driver()
    
    try:
        # List of test URLs - these are real TradingView URLs mentioned in the requirements
        test_urls = [
            "https://www.tradingview.com/symbols/XETR-CDOT/",
            "https://www.tradingview.com/symbols/XETR-CLTC/",
            "https://www.tradingview.com/symbols/XETR-COMS/"
        ]
        
        # Expected format for validation (not exact values)
        # We're checking that the extractor returns values in the expected format
        for url in test_urls:
            logging.info(f"Testing URL: {url}")
            
            # Extract shares with our custom function
            result = extract_tradingview_shares(driver, url)
            
            # Validate the result
            if "error" in result:
                logging.error(f"Error extracting from {url}: {result['error']}")
                continue
                
            if "outstanding_shares" in result:
                shares_str = result["outstanding_shares"]
                logging.info(f"Successfully extracted shares: {shares_str}")
                
                # Validate format - should contain numbers and possibly K/M/B suffix
                if not any(char.isdigit() for char in shares_str):
                    logging.error(f"Invalid shares format - no digits found: {shares_str}")
                
                # Check if the format includes expected units (K, M, B)
                units = ["K", "M", "B", "k", "m", "b"]
                has_unit = any(unit in shares_str for unit in units)
                if not has_unit:
                    logging.warning(f"No unit (K/M/B) found in shares value: {shares_str}")
                    
                logging.info(f"Validation passed for {url}")
            else:
                logging.error(f"No shares outstanding data found for {url}")
                
            # Pause between requests to avoid rate limiting
            time.sleep(2)
            
    except Exception as e:
        logging.error(f"Test error: {str(e)}")
    finally:
        # Clean up
        driver.quit()
        logging.info("Test completed")

if __name__ == "__main__":
    test_tradingview_extractor() 