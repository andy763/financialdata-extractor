#!/usr/bin/env python3
"""
Quick investigation of promising 2-error websites
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

def investigate_issuance_swiss(driver, url):
    """
    Investigate issuance.swiss - 2 errors
    URLs: https://issuance.swiss/figment_ethf/ and https://issuance.swiss/figment_solf/
    """
    print(f"\n🔍 INVESTIGATING: Issuance Swiss")
    print(f"URL: {url}")
    
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)
    except Exception:
        print("❌ Page load timeout")
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    print("\n📊 Looking for price patterns:")
    
    # Look for Swiss/crypto fund patterns
    patterns = [
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'NAV[^0-9]*?([\d,\.]+)', 'NAV'),
        (r'Value[^0-9]*?([\d,\.]+)', 'Value'),
        (r'CHF\s*([\d,\.]+)', 'CHF'),
        (r'USD\s*([\d,\.]+)', 'USD'),
        (r'EUR\s*([\d,\.]+)', 'EUR'),
        (r'\$\s*([\d,\.]+)', 'Dollar'),
    ]
    
    for pattern, desc in patterns:
        matches = re.finditer(pattern, page_text, re.IGNORECASE)
        for match in matches:
            price_str = match.group(1)
            try:
                price_value = float(price_str.replace(',', ''))
                if 0.1 <= price_value <= 10000:
                    context_start = max(0, match.start() - 80)
                    context_end = min(len(page_text), match.end() + 80)
                    context = page_text[context_start:context_end].strip()
                    print(f"  {desc}: {price_value} - Context: ...{context}...")
            except ValueError:
                continue

def investigate_abraxascm(driver, url):
    """
    Investigate abraxascm.com - 2 errors
    URLs: https://www.abraxascm.com/alpha-bitcoin-fund/ and https://www.abraxascm.com/alpha-ethereum-fund/
    """
    print(f"\n🔍 INVESTIGATING: Abraxas Capital Management")
    print(f"URL: {url}")
    
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)
    except Exception:
        print("❌ Page load timeout")
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    print("\n📊 Looking for price patterns:")
    
    # Look for fund management patterns
    patterns = [
        (r'NAV[^0-9]*?([\d,\.]+)', 'NAV'),
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'Unit\s+Price[^0-9]*?([\d,\.]+)', 'Unit Price'),
        (r'Share\s+Price[^0-9]*?([\d,\.]+)', 'Share Price'),
        (r'USD\s*([\d,\.]+)', 'USD'),
        (r'\$\s*([\d,\.]+)', 'Dollar'),
    ]
    
    for pattern, desc in patterns:
        matches = re.finditer(pattern, page_text, re.IGNORECASE)
        for match in matches:
            price_str = match.group(1)
            try:
                price_value = float(price_str.replace(',', ''))
                if 0.1 <= price_value <= 10000:
                    context_start = max(0, match.start() - 80)
                    context_end = min(len(page_text), match.end() + 80)
                    context = page_text[context_start:context_end].strip()
                    print(f"  {desc}: {price_value} - Context: ...{context}...")
            except ValueError:
                continue

def investigate_markets_businessinsider(driver, url):
    """
    Investigate markets.businessinsider.com - 2 errors
    URLs: ETF pages
    """
    print(f"\n🔍 INVESTIGATING: Markets Business Insider")
    print(f"URL: {url}")
    
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)
    except Exception:
        print("❌ Page load timeout")
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    print("\n📊 Looking for price patterns:")
    
    # Look for Business Insider ETF patterns
    patterns = [
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'Last[^0-9]*?([\d,\.]+)', 'Last'),
        (r'Close[^0-9]*?([\d,\.]+)', 'Close'),
        (r'Current[^0-9]*?([\d,\.]+)', 'Current'),
        (r'USD\s*([\d,\.]+)', 'USD'),
        (r'\$\s*([\d,\.]+)', 'Dollar'),
    ]
    
    for pattern, desc in patterns:
        matches = re.finditer(pattern, page_text, re.IGNORECASE)
        for match in matches:
            price_str = match.group(1)
            try:
                price_value = float(price_str.replace(',', ''))
                if 0.1 <= price_value <= 10000:
                    context_start = max(0, match.start() - 80)
                    context_end = min(len(page_text), match.end() + 80)
                    context = page_text[context_start:context_end].strip()
                    print(f"  {desc}: {price_value} - Context: ...{context}...")
            except ValueError:
                continue

def run_2_error_investigations():
    """Run investigations on promising 2-error websites"""
    
    # URLs to investigate (2-error websites)
    test_urls = [
        ("https://issuance.swiss/figment_ethf/", investigate_issuance_swiss),
        ("https://www.abraxascm.com/alpha-bitcoin-fund/", investigate_abraxascm),
        ("https://markets.businessinsider.com/etfs/ark-21shares-active-bitcoin-ethereum-strategy-etf-us02072l3428", investigate_markets_businessinsider),
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
        
        print("🔬 INVESTIGATING 2-ERROR WEBSITES (MEDIUM DIFFICULTY)")
        print("=" * 80)
        
        for url, func in test_urls:
            try:
                func(driver, url)
            except Exception as e:
                print(f"❌ Investigation failed for {url}: {e}")
                
    except Exception as e:
        print(f"Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_2_error_investigations() 