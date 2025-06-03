#!/usr/bin/env python3
"""
Custom functions to fix .0 errors for specific websites
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

def get_schwab_asset_management_price(driver, url):
    """
    Navigate to a Schwab Asset Management ETF page and scrape the actual market price.
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for Schwab page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price patterns
    try:
        page_text = soup.get_text(" ", strip=True)
        
        # Look for various price patterns
        price_patterns = [
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Last\s+Price[^$]*\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'Current\s+Price[^$]*\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'NAV[^$]*\$\s*([\d,\.]+)',                # "NAV $XX.XX" (as fallback)
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    # Look for reasonable ETF prices with decimals
                    if 1 <= price_value <= 500 and price_value != int(price_value):
                        logging.info(f"Found Schwab price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with Schwab pattern method: {e}")
    
    raise ValueError("Could not find valid market price on Schwab page")

def get_ninepoint_price(driver, url):
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
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for Ninepoint page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price patterns
    try:
        page_text = soup.get_text(" ", strip=True)
        
        # Look for various price patterns (Canadian format)
        price_patterns = [
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Last\s+Price[^$]*\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'Current\s+Price[^$]*\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'Unit\s+Price[^$]*\$\s*([\d,\.]+)',       # "Unit Price $XX.XX"
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    # Look for reasonable ETF prices with decimals
                    if 1 <= price_value <= 500 and price_value != int(price_value):
                        logging.info(f"Found Ninepoint price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with Ninepoint pattern method: {e}")
    
    raise ValueError("Could not find valid market price on Ninepoint page")

def get_evolve_etfs_price(driver, url):
    """
    Navigate to an Evolve ETFs page and scrape the actual market price.
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for Evolve ETFs page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price patterns
    try:
        page_text = soup.get_text(" ", strip=True)
        
        # Look for various price patterns (Canadian format)
        price_patterns = [
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Last\s+Price[^$]*\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'Current\s+Price[^$]*\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'Closing\s+Price[^$]*\$\s*([\d,\.]+)',    # "Closing Price $XX.XX"
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    # Look for reasonable ETF prices with decimals
                    if 1 <= price_value <= 500 and price_value != int(price_value):
                        logging.info(f"Found Evolve ETFs price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with Evolve ETFs pattern method: {e}")
    
    raise ValueError("Could not find valid market price on Evolve ETFs page")

def get_21shares_price(driver, url):
    """
    Navigate to a 21Shares ETF page and scrape the actual market price.
    Returns a float or raises ValueError.
    """
    driver.get(url)
    try:
        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for 21Shares page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price patterns
    try:
        page_text = soup.get_text(" ", strip=True)
        
        # Look for various price patterns (US format)
        price_patterns = [
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Last\s+Price[^$]*\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'Current\s+Price[^$]*\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'Closing\s+Price[^$]*\$\s*([\d,\.]+)',    # "Closing Price $XX.XX"
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    # Look for reasonable ETF prices with decimals
                    if 1 <= price_value <= 500 and price_value != int(price_value):
                        logging.info(f"Found 21Shares price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with 21Shares pattern method: {e}")
    
    raise ValueError("Could not find valid market price on 21Shares page")

def get_betashares_price(driver, url):
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
        time.sleep(8)
    except Exception:
        raise ValueError("Timed out waiting for BetaShares page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price patterns
    try:
        page_text = soup.get_text(" ", strip=True)
        
        # Look for various price patterns (Australian format)
        price_patterns = [
            r'Market\s+Price[^$]*\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'Price[^$]*\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Last\s+Price[^$]*\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'Current\s+Price[^$]*\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'Closing\s+Price[^$]*\$\s*([\d,\.]+)',    # "Closing Price $XX.XX"
            r'Unit\s+Price[^$]*\$\s*([\d,\.]+)',       # "Unit Price $XX.XX"
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    # Look for reasonable ETF prices with decimals
                    if 1 <= price_value <= 500 and price_value != int(price_value):
                        logging.info(f"Found BetaShares price: ${price_value}")
                        return price_value
                except ValueError:
                    continue
    except Exception as e:
        logging.error(f"Error with BetaShares pattern method: {e}")
    
    raise ValueError("Could not find valid market price on BetaShares page")

def test_website_fixes():
    """Test the custom functions for the problematic websites"""
    
    # URLs with .0 errors
    test_urls = [
        ("https://www.schwabassetmanagement.com/products/stce", get_schwab_asset_management_price, "Schwab Asset Management"),
        ("https://www.ninepoint.com/funds/ninepoint-crypto-and-ai-leaders-etf/", get_ninepoint_price, "Ninepoint"),
        ("https://evolveetfs.com/product/ethr#tab-content-overview/", get_evolve_etfs_price, "Evolve ETFs"),
        ("https://www.21shares.com/en-us/product/arkb", get_21shares_price, "21Shares"),
        ("https://www.betashares.com.au/fund/crypto-innovators-etf/#resources", get_betashares_price, "BetaShares"),
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
        
        print("🔧 Testing custom functions for .0 error websites:")
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
    test_website_fixes() 