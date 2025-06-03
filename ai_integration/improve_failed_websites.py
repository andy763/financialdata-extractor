#!/usr/bin/env python3
"""
Improved functions for the two websites that failed (Ninepoint and BetaShares)
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import logging

def get_ninepoint_price_improved(driver, url):
    """
    Navigate to a Ninepoint ETF page and scrape the actual market price.
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(10)  # Increased wait time
    except Exception:
        raise ValueError("Timed out waiting for Ninepoint page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price patterns with more flexible matching
    try:
        page_text = soup.get_text(" ", strip=True)
        
        # Look for various price patterns (Canadian format) - more flexible
        price_patterns = [
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Last\s+Price[^$]*\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'Current\s+Price[^$]*\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'Unit\s+Price[^$]*\$\s*([\d,\.]+)',       # "Unit Price $XX.XX"
            r'NAV[^$]*\$\s*([\d,\.]+)',                # "NAV $XX.XX"
            r'Net\s+Asset\s+Value[^$]*\$\s*([\d,\.]+)', # "Net Asset Value $XX.XX"
            r'\$\s*([\d,\.]+)\s*CAD',                  # "$XX.XX CAD"
            r'CAD\s*\$\s*([\d,\.]+)',                  # "CAD $XX.XX"
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    # Look for reasonable ETF prices (relaxed criteria)
                    if 0.1 <= price_value <= 1000:  # More flexible range
                        logging.info(f"Found Ninepoint price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with Ninepoint pattern method: {e}")
    
    # Method 2: Look for any dollar amounts in the page
    try:
        all_dollar_matches = re.finditer(r'\$\s*([\d,\.]+)', page_text, re.IGNORECASE)
        for match in all_dollar_matches:
            price_str = match.group(1)
            try:
                price_value = float(price_str.replace(',', ''))
                # Look for reasonable ETF prices
                if 1 <= price_value <= 500 and price_value != int(price_value):
                    logging.info(f"Found Ninepoint price (general search): ${price_value}")
                    return price_value
            except ValueError:
                continue
    except Exception as e:
        logging.error(f"Error with Ninepoint general search: {e}")
    
    raise ValueError("Could not find valid market price on Ninepoint page")

def get_betashares_price_improved(driver, url):
    """
    Navigate to a BetaShares ETF page and scrape the actual market price.
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(10)  # Increased wait time
    except Exception:
        raise ValueError("Timed out waiting for BetaShares page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price patterns with more flexible matching
    try:
        page_text = soup.get_text(" ", strip=True)
        
        # Look for various price patterns (Australian format) - more flexible
        price_patterns = [
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Last\s+Price[^$]*\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'Current\s+Price[^$]*\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'Closing\s+Price[^$]*\$\s*([\d,\.]+)',    # "Closing Price $XX.XX"
            r'Unit\s+Price[^$]*\$\s*([\d,\.]+)',       # "Unit Price $XX.XX"
            r'NAV[^$]*\$\s*([\d,\.]+)',                # "NAV $XX.XX"
            r'Net\s+Asset\s+Value[^$]*\$\s*([\d,\.]+)', # "Net Asset Value $XX.XX"
            r'\$\s*([\d,\.]+)\s*AUD',                  # "$XX.XX AUD"
            r'AUD\s*\$\s*([\d,\.]+)',                  # "AUD $XX.XX"
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    # Look for reasonable ETF prices (relaxed criteria)
                    if 0.1 <= price_value <= 1000:  # More flexible range
                        logging.info(f"Found BetaShares price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with BetaShares pattern method: {e}")
    
    # Method 2: Look for any dollar amounts in the page
    try:
        all_dollar_matches = re.finditer(r'\$\s*([\d,\.]+)', page_text, re.IGNORECASE)
        for match in all_dollar_matches:
            price_str = match.group(1)
            try:
                price_value = float(price_str.replace(',', ''))
                # Look for reasonable ETF prices
                if 1 <= price_value <= 500 and price_value != int(price_value):
                    logging.info(f"Found BetaShares price (general search): ${price_value}")
                    return price_value
            except ValueError:
                continue
    except Exception as e:
        logging.error(f"Error with BetaShares general search: {e}")
    
    raise ValueError("Could not find valid market price on BetaShares page")

def test_improved_functions():
    """Test the improved functions for the problematic websites"""
    
    # URLs that failed before
    test_urls = [
        ("https://www.ninepoint.com/funds/ninepoint-crypto-and-ai-leaders-etf/", get_ninepoint_price_improved, "Ninepoint (Improved)"),
        ("https://www.betashares.com.au/fund/crypto-innovators-etf/#resources", get_betashares_price_improved, "BetaShares (Improved)"),
    ]
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        
        print("🔧 Testing improved functions for failed websites:")
        print("=" * 80)
        
        for url, func, name in test_urls:
            print(f"\n🌐 Testing {name}: {url}")
            try:
                price = func(driver, url)
                print(f"  ✅ SUCCESS: Found price ${price}")
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                
    except Exception as e:
        print(f"Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_improved_functions() 