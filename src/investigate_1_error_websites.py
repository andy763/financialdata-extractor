#!/usr/bin/env python3
"""
Investigation script for 1-error websites (easiest fixes first)
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

def investigate_valour(driver, url):
    """
    Investigate Valour.com - ETF/ETP provider
    URL: https://valour.com/en/products/valour-ethereum-physical-staking
    """
    print(f"\n🔍 INVESTIGATING: Valour.com")
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
    
    # Look for various price patterns
    patterns = [
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'NAV[^0-9]*?([\d,\.]+)', 'NAV'),
        (r'Market\s+Price[^0-9]*?([\d,\.]+)', 'Market Price'),
        (r'Current[^0-9]*?([\d,\.]+)', 'Current'),
        (r'Last[^0-9]*?([\d,\.]+)', 'Last'),
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

def investigate_hashdex(driver, url):
    """
    Investigate Hashdex.com - Crypto fund provider
    URL: https://www.hashdex.com/en-KY/products/hdexbh
    """
    print(f"\n🔍 INVESTIGATING: Hashdex.com")
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
    
    # Look for various price patterns
    patterns = [
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'NAV[^0-9]*?([\d,\.]+)', 'NAV'),
        (r'Market\s+Value[^0-9]*?([\d,\.]+)', 'Market Value'),
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

def investigate_nasdaq_european(driver, url):
    """
    Investigate NASDAQ European Market
    URL: https://www.nasdaq.com/european-market-activity/etn-etc/viralt?id=SSE366514
    """
    print(f"\n🔍 INVESTIGATING: NASDAQ European Market")
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
    
    # Look for NASDAQ-specific patterns
    patterns = [
        (r'Last\s+Sale[^0-9]*?([\d,\.]+)', 'Last Sale'),
        (r'Current\s+Price[^0-9]*?([\d,\.]+)', 'Current Price'),
        (r'Market\s+Price[^0-9]*?([\d,\.]+)', 'Market Price'),
        (r'Close[^0-9]*?([\d,\.]+)', 'Close'),
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'SEK\s*([\d,\.]+)', 'SEK'),
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

def investigate_finexetf(driver, url):
    """
    Investigate FinexETF.com
    URL: https://finexetf.com/product/FXBC/
    """
    print(f"\n🔍 INVESTIGATING: FinexETF.com")
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
    
    # Look for ETF-specific patterns
    patterns = [
        (r'NAV[^0-9]*?([\d,\.]+)', 'NAV'),
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'Market\s+Price[^0-9]*?([\d,\.]+)', 'Market Price'),
        (r'Unit\s+Price[^0-9]*?([\d,\.]+)', 'Unit Price'),
        (r'Last\s+Price[^0-9]*?([\d,\.]+)', 'Last Price'),
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

def investigate_purposeinvest(driver, url):
    """
    Investigate Purpose Investments (Canadian ETF provider)
    URL: https://www.purposeinvest.com/funds/purpose-ether-staking-corp-etf
    """
    print(f"\n🔍 INVESTIGATING: Purpose Investments")
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
    
    # Look for Canadian ETF patterns
    patterns = [
        (r'NAV[^0-9]*?([\d,\.]+)', 'NAV'),
        (r'Price[^0-9]*?([\d,\.]+)', 'Price'),
        (r'Market\s+Price[^0-9]*?([\d,\.]+)', 'Market Price'),
        (r'Unit\s+Price[^0-9]*?([\d,\.]+)', 'Unit Price'),
        (r'Closing\s+Price[^0-9]*?([\d,\.]+)', 'Closing Price'),
        (r'CAD\s*([\d,\.]+)', 'CAD'),
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

def run_investigations():
    """Run investigations on 1-error websites"""
    
    # URLs to investigate (1-error websites)
    test_urls = [
        ("https://valour.com/en/products/valour-ethereum-physical-staking", investigate_valour),
        ("https://www.hashdex.com/en-KY/products/hdexbh", investigate_hashdex),
        ("https://www.nasdaq.com/european-market-activity/etn-etc/viralt?id=SSE366514", investigate_nasdaq_european),
        ("https://finexetf.com/product/FXBC/", investigate_finexetf),
        ("https://www.purposeinvest.com/funds/purpose-ether-staking-corp-etf", investigate_purposeinvest),
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
        
        print("🔬 INVESTIGATING 1-ERROR WEBSITES (EASIEST FIXES FIRST)")
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
    run_investigations() 