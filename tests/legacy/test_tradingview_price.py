import logging
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def get_tradingview_price(driver, url):
    """
    Navigate to a TradingView symbol page and scrape the share price.
    Returns a float or raises ValueError.
    """
    try:
        logging.info(f"TradingView: Navigating to {url}")
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(8)  # TradingView uses a lot of JS
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Method 1: Look for price in TradingView-specific selectors
        try:
            price_selectors = [
                "[data-field='last_price']",
                ".tv-symbol-price-quote__value",
                ".js-symbol-last",
                ".last-price",
                ".current-price",
                ".price-value",
                "[class*='price'][class*='last']",
                "[class*='quote'][class*='price']"
            ]
            
            for selector in price_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    logging.info(f"TradingView: Found element with selector '{selector}': {text}")
                    
                    # Look for price patterns (USD, numbers with decimals)
                    price_match = re.search(r'([\d,]+\.[\d]{2,})', text)
                    if price_match:
                        price_str = price_match.group(1)
                        try:
                            price_value = float(price_str.replace(',', ''))
                            if 0.01 <= price_value <= 100000:
                                logging.info(f"TradingView: Found price using selector '{selector}': {price_value}")
                                return price_value
                        except ValueError:
                            continue
                            
        except Exception as e:
            logging.error(f"TradingView: Error with selector method: {e}")
        
        # Method 2: Look for price patterns in text content
        try:
            page_text = soup.get_text(" ", strip=True)
            
            # Look for patterns like "27.88USD", "27.88 USD", etc.
            price_patterns = [
                r'([\d,]+\.[\d]{2,})\s*USD',          # "27.88USD" or "27.88 USD"
                r'([\d,]+\.[\d]{2,})\s*\$',           # "27.88$"
                r'\$\s*([\d,]+\.[\d]{2,})',           # "$27.88"
                r'Price\s*:?\s*([\d,]+\.[\d]{2,})',   # "Price: 27.88"
                r'Last\s*:?\s*([\d,]+\.[\d]{2,})',    # "Last: 27.88"
                r'([\d,]+\.[\d]{2,})\s*−[\d,]+\.[\d]{2,}', # "27.88−0.08−0.29%" pattern
            ]
            
            for pattern in price_patterns:
                matches = re.finditer(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    price_str = match.group(1)
                    try:
                        price_value = float(price_str.replace(',', ''))
                        if 0.01 <= price_value <= 100000:
                            logging.info(f"TradingView: Found price using pattern '{pattern}': {price_value}")
                            return price_value
                    except ValueError:
                        continue
                        
        except Exception as e:
            logging.error(f"TradingView: Error with text pattern method: {e}")
        
        # Method 3: Look for JSON data in script tags (TradingView often embeds data)
        try:
            script_tags = soup.find_all('script')
            for script in script_tags:
                script_content = script.get_text() if script.string else ""
                if 'last_price' in script_content or 'lastPrice' in script_content:
                    # Look for price values in JSON
                    price_matches = re.findall(r'"(?:last_price|lastPrice)"\s*:\s*([\d.]+)', script_content)
                    for price_str in price_matches:
                        try:
                            price_value = float(price_str)
                            if 0.01 <= price_value <= 100000:
                                logging.info(f"TradingView: Found price in script data: {price_value}")
                                return price_value
                        except ValueError:
                            continue
                            
        except Exception as e:
            logging.error(f"TradingView: Error with script parsing method: {e}")
        
        # Method 4: Look for any decimal numbers that could be prices
        try:
            # Extract all decimal numbers from the page
            all_numbers = re.findall(r'\b([\d,]+\.\d{2,})\b', page_text)
            valid_prices = []
            
            for num_str in all_numbers:
                try:
                    price_value = float(num_str.replace(',', ''))
                    if 0.01 <= price_value <= 100000:
                        valid_prices.append(price_value)
                except ValueError:
                    continue
            
            if valid_prices:
                # Return the most likely price (often the first one that appears)
                price_value = valid_prices[0]
                logging.info(f"TradingView: Found price using general number extraction: {price_value}")
                return price_value
                
        except Exception as e:
            logging.error(f"TradingView: Error with general number extraction: {e}")
        
        raise ValueError("Could not find price on TradingView page")
        
    except Exception as e:
        logging.error(f"TradingView: Unexpected error: {e}")
        raise ValueError(f"TradingView scraping failed: {e}")

def test_tradingview_price_urls():
    """Test TradingView URLs for price extraction"""
    
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
            logging.info(f"\n--- Testing URL: {url} ---")
            try:
                price = get_tradingview_price(driver, url)
                logging.info(f"SUCCESS: Extracted price {price} from {url}")
            except Exception as e:
                logging.error(f"FAILED: {e} for {url}")
                
                # Debug: Save page source
                symbol = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
                with open(f"tradingview_debug_{symbol}.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                logging.info(f"Saved debug HTML for {url}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    test_tradingview_price_urls()
