#!/usr/bin/env python3
"""
Debug script for Grayscale fund pages to understand why price extraction is failing
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

def test_grayscale_url(url):
    """Test a single Grayscale URL to see what's happening"""
    print(f"\n{'='*80}")
    print(f"Testing: {url}")
    print(f"{'='*80}")
    
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
        driver.set_page_load_timeout(30)
        
        # Load the page
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Wait for JavaScript to load
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        
        print("Page loaded successfully")
        print(f"Page text length: {len(page_text)} characters")
        
        # Search for Market Price patterns
        print("\n--- Searching for Market Price patterns ---")
        
        # Pattern 1: Market Price as of MM/DD/YYYY $XX.XX
        pattern1 = re.search(
            r'Market Price\s+as\s+of\s+\d{1,2}/\d{1,2}/\d{4}\s*\$\s*([\d,\.]+)', 
            page_text, re.IGNORECASE
        )
        if pattern1:
            print(f"✅ FOUND Pattern 1: Market Price as of DATE $PRICE: ${pattern1.group(1)}")
        else:
            print("❌ Pattern 1 NOT found: Market Price as of DATE $PRICE")
        
        # Pattern 2: $XX.XX Market Price as of MM/DD/YYYY
        pattern2 = re.search(
            r'\$\s*([\d,\.]+)\s+Market Price\s+as\s+of\s+\d{1,2}/\d{1,2}/\d{4}', 
            page_text, re.IGNORECASE
        )
        if pattern2:
            print(f"✅ FOUND Pattern 2: $PRICE Market Price as of DATE: ${pattern2.group(1)}")
        else:
            print("❌ Pattern 2 NOT found: $PRICE Market Price as of DATE")
        
        # Search for any mention of "Market Price"
        market_price_matches = re.finditer(r'market\s+price', page_text, re.IGNORECASE)
        market_price_contexts = []
        for match in market_price_matches:
            start = max(0, match.start() - 50)
            end = min(len(page_text), match.end() + 50)
            context = page_text[start:end].replace('\n', ' ').strip()
            market_price_contexts.append(context)
        
        if market_price_contexts:
            print(f"\n--- Found {len(market_price_contexts)} 'Market Price' mentions ---")
            for i, context in enumerate(market_price_contexts[:5]):  # Show first 5
                print(f"{i+1}. ...{context}...")
        else:
            print("\n❌ NO 'Market Price' mentions found")
        
        # Search for any dollar amounts
        dollar_matches = re.finditer(r'\$\s*([\d,\.]+)', page_text)
        dollar_amounts = []
        for match in dollar_matches:
            amount = match.group(1)
            start = max(0, match.start() - 30)
            end = min(len(page_text), match.end() + 30)
            context = page_text[start:end].replace('\n', ' ').strip()
            dollar_amounts.append((amount, context))
        
        if dollar_amounts:
            print(f"\n--- Found {len(dollar_amounts)} dollar amounts ---")
            for i, (amount, context) in enumerate(dollar_amounts[:10]):  # Show first 10
                print(f"{i+1}. ${amount} in context: ...{context}...")
        else:
            print("\n❌ NO dollar amounts found")
        
        # Search for price-related keywords
        price_keywords = ['price', 'value', 'nav', 'quote', 'last', 'current', 'trading']
        print(f"\n--- Searching for price keywords ---")
        for keyword in price_keywords:
            matches = re.finditer(rf'\b{keyword}\b', page_text, re.IGNORECASE)
            count = len(list(matches))
            print(f"'{keyword}': {count} mentions")
        
        # Look for specific Grayscale page elements
        print(f"\n--- Looking for Grayscale-specific elements ---")
        
        # Check if it's a Grayscale fund page structure
        fund_title = soup.find(['h1', 'title'])
        if fund_title:
            print(f"Page title: {fund_title.get_text(strip=True)}")
        
        # Look for any JSON data that might contain prices
        script_tags = soup.find_all('script')
        json_data_found = False
        for script in script_tags:
            if script.string and ('price' in script.string.lower() or 'market' in script.string.lower()):
                print(f"Found script with price/market data: {script.string[:200]}...")
                json_data_found = True
                break
        
        if not json_data_found:
            print("No JSON/script data with price information found")
        
        # Save a snippet of the page for manual inspection
        print(f"\n--- First 1000 characters of page ---")
        print(page_text[:1000])
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {url}: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    """Test the problematic Grayscale URLs"""
    problematic_urls = [
        "https://www.grayscale.com/funds/grayscale-chainlink-trust",
        "https://www.grayscale.com/funds/grayscale-digital-large-cap-fund", 
        "https://www.grayscale.com/funds/grayscale-filecoin-trust",
        "https://www.grayscale.com/funds/grayscale-horizen-trust",
        "https://www.grayscale.com/funds/grayscale-litecoin-trust"
    ]
    
    print("🔍 Starting Grayscale URL debugging...")
    
    for url in problematic_urls:
        success = test_grayscale_url(url)
        if not success:
            print(f"Failed to test {url}")
        
        print(f"\n{'='*80}")
        input("Press Enter to continue to next URL...")

if __name__ == "__main__":
    main() 