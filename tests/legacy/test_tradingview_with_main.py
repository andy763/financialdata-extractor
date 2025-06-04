import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from outstanding_shares_updater import extract_outstanding_shares_with_ai_fallback

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

def test_tradingview_with_main():
    """
    Test the TradingView custom extractor with the main outstanding shares updater.
    This ensures that our new extractor is correctly integrated with the main script.
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
        
        for url in test_urls:
            logging.info(f"\nTesting URL: {url}")
            
            # Test with the main extraction pipeline
            result = extract_outstanding_shares_with_ai_fallback(driver, url)
            
            # Check if the result is successful and which method was used
            if "error" in result:
                logging.error(f"Error: {result['error']}")
            else:
                logging.info(f"Successfully extracted shares: {result['outstanding_shares']}")
                logging.info(f"Method used: {result.get('method', 'unknown')}")
                
                # Verify that the custom extractor was used
                if result.get('method') in ['custom', 'improved_custom']:
                    logging.info("✅ SUCCESS: TradingView custom extractor was used!")
                else:
                    logging.warning(f"⚠️ WARNING: TradingView custom extractor was not used. Method: {result.get('method')}")
            
            # Pause between requests to avoid rate limiting
            time.sleep(2)
            
    except Exception as e:
        logging.error(f"Test error: {str(e)}")
    finally:
        # Clean up
        driver.quit()
        logging.info("Test completed")

if __name__ == "__main__":
    test_tradingview_with_main() 