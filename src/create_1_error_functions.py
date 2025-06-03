#!/usr/bin/env python3
"""
Custom functions for 1-error websites based on investigation results
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

def get_valour_price(driver, url):
    """
    Navigate to a Valour ETF page and scrape the share price.
    Pattern found: "Share Price 1.2649 EUR"
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for Valour page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    # Method 1: Look for "Share Price X.XXXX EUR" pattern (most reliable)
    try:
        share_price_pattern = r'Share\s+Price\s+([\d,\.]+)\s+EUR'
        match = re.search(share_price_pattern, page_text, re.IGNORECASE)
        if match:
            price_str = match.group(1)
            price_value = float(price_str.replace(',', ''))
            if 0.01 <= price_value <= 1000:  # Reasonable ETF price range
                logging.info(f"Found Valour share price: {price_value} EUR")
                return price_value
    except Exception as e:
        logging.error(f"Error with Valour share price method: {e}")
    
    # Method 2: Look for general price patterns near "Price"
    try:
        price_patterns = [
            r'Price[^0-9]*?([\d,\.]+)',           # "Price 1.2649"
            r'Current\s+Price[^0-9]*?([\d,\.]+)', # "Current Price 1.2649"
            r'Unit\s+Price[^0-9]*?([\d,\.]+)',    # "Unit Price 1.2649"
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.01 <= price_value <= 1000:
                        logging.info(f"Found Valour price: {price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with Valour general price method: {e}")
    
    raise ValueError("Could not find valid share price on Valour page")

def get_nasdaq_european_price(driver, url):
    """
    Navigate to a NASDAQ European Market page and scrape the price.
    Pattern found: "SEK 15.86"
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for NASDAQ European page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    # Method 1: Look for "SEK XX.XX" pattern (most reliable for this specific URL)
    try:
        sek_pattern = r'SEK\s+([\d,\.]+)'
        match = re.search(sek_pattern, page_text, re.IGNORECASE)
        if match:
            price_str = match.group(1)
            price_value = float(price_str.replace(',', ''))
            if 0.01 <= price_value <= 10000:  # Reasonable price range for SEK
                logging.info(f"Found NASDAQ European price: {price_value} SEK")
                return price_value
    except Exception as e:
        logging.error(f"Error with NASDAQ European SEK method: {e}")
    
    # Method 2: Look for other currency patterns
    try:
        currency_patterns = [
            (r'USD\s+([\d,\.]+)', 'USD'),
            (r'EUR\s+([\d,\.]+)', 'EUR'),
            (r'Last\s+Sale[^0-9]*?([\d,\.]+)', 'Last Sale'),
            (r'Current\s+Price[^0-9]*?([\d,\.]+)', 'Current Price'),
        ]
        
        for pattern, desc in currency_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.01 <= price_value <= 10000:
                        logging.info(f"Found NASDAQ European {desc}: {price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with NASDAQ European currency method: {e}")
    
    raise ValueError("Could not find valid price on NASDAQ European page")

def get_purposeinvest_price(driver, url):
    """
    Navigate to a Purpose Investments ETF page and scrape the NAV.
    Pattern found: "NAV $4.80"
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for Purpose Investments page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    # Method 1: Look for "NAV $X.XX" pattern (most reliable)
    try:
        nav_pattern = r'NAV\s+\$\s*([\d,\.]+)'
        match = re.search(nav_pattern, page_text, re.IGNORECASE)
        if match:
            price_str = match.group(1)
            price_value = float(price_str.replace(',', ''))
            if 0.01 <= price_value <= 1000:  # Reasonable ETF NAV range
                logging.info(f"Found Purpose Investments NAV: ${price_value}")
                return price_value
    except Exception as e:
        logging.error(f"Error with Purpose Investments NAV method: {e}")
    
    # Method 2: Look for other price patterns
    try:
        price_patterns = [
            r'Unit\s+Price[^$]*\$\s*([\d,\.]+)',    # "Unit Price $X.XX"
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',  # "Market Price $X.XX"
            r'Closing\s+Price[^$]*\$\s*([\d,\.]+)', # "Closing Price $X.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',           # "Price $X.XX"
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.01 <= price_value <= 1000:
                        logging.info(f"Found Purpose Investments price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with Purpose Investments price method: {e}")
    
    raise ValueError("Could not find valid NAV/price on Purpose Investments page")

def test_1_error_functions():
    """Test the custom functions for 1-error websites"""
    
    # URLs with the custom functions
    test_urls = [
        ("https://valour.com/en/products/valour-ethereum-physical-staking", get_valour_price, "Valour"),
        ("https://www.nasdaq.com/european-market-activity/etn-etc/viralt?id=SSE366514", get_nasdaq_european_price, "NASDAQ European"),
        ("https://www.purposeinvest.com/funds/purpose-ether-staking-corp-etf", get_purposeinvest_price, "Purpose Investments"),
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
        
        print("🎯 Testing custom functions for 1-error websites:")
        print("=" * 80)
        
        for url, func, name in test_urls:
            print(f"\n🌐 Testing {name}: {url}")
            try:
                price = func(driver, url)
                print(f"  ✅ SUCCESS: Found price {price}")
                
                # Check if it's a reasonable value
                if 0.01 <= price <= 10000:
                    print(f"  🎉 EXCELLENT: Reasonable price value!")
                else:
                    print(f"  ⚠️  WARNING: Price seems unusual")
                    
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                
    except Exception as e:
        print(f"Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_1_error_functions() 