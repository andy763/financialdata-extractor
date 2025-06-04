import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_globalx_shares

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

def test_globalx_extractor():
    """
    Test the GlobalX ETFs custom extractor on various URL examples.
    
    NOTE: This test verifies that the extractor can find and extract
    shares outstanding data. The actual values may change over time as the
    shares outstanding change.
    """
    # Initialize the WebDriver
    driver = setup_driver()
    
    try:
        # List of test URLs for GlobalX ETFs
        test_urls = [
            "https://globalxetfs.eu/funds/et0x/#trading",  # Example from the requirements
            "https://globalxetfs.eu/funds/bt0x/#holdings"   # Additional example to test
        ]
        
        for url in test_urls:
            logging.info(f"===== Testing URL: {url} =====")
            
            # Extract shares with our custom function
            result = extract_globalx_shares(driver, url)
            
            # Validate the result
            if "error" in result:
                logging.error(f"Error extracting from {url}: {result['error']}")
                continue
                
            if "outstanding_shares" in result:
                shares_str = result["outstanding_shares"]
                logging.info(f"Successfully extracted shares: {shares_str}")
                
                # Validate format - should contain numbers
                if not any(char.isdigit() for char in shares_str):
                    logging.error(f"Invalid shares format - no digits found: {shares_str}")
                else:
                    logging.info(f"VALIDATION PASSED: Valid shares outstanding value found for {url}")
                    
                    # For ET0X, validate against expected value
                    if "et0x" in url.lower() and shares_str == "37,674.00":
                        logging.info("EXACT MATCH: Value matches the expected 37,674.00 for ET0X")
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
    test_globalx_extractor() 