#!/usr/bin/env python3
"""
Debug script for Franklin Templeton ETF pages to understand why price extraction is failing
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

def test_franklin_templeton_url(url):
    """Test a single Franklin Templeton URL to see what's happening"""
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    
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
        driver.set_page_load_timeout(45)
        
        # Load the page
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Wait for JavaScript to load
        time.sleep(8)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        
        print(f"✅ Page loaded: {len(page_text)} chars")
        
        # Look for various price patterns that might be on Franklin Templeton pages
        price_patterns = [
            r'Market\s+Price.*?\$\s*([\d,\.]+)',     # "Market Price $XX.XX"
            r'NAV.*?\$\s*([\d,\.]+)',                # "NAV $XX.XX"
            r'Price.*?\$\s*([\d,\.]+)',              # "Price $XX.XX"
            r'Share\s+Price.*?\$\s*([\d,\.]+)',      # "Share Price $XX.XX"
            r'Current\s+Price.*?\$\s*([\d,\.]+)',    # "Current Price $XX.XX"
            r'Last\s+Price.*?\$\s*([\d,\.]+)',       # "Last Price $XX.XX"
            r'\$\s*([\d,\.]+)',                      # Any dollar amount
        ]
        
        found_prices = []
        for pattern in price_patterns:
            matches = list(re.finditer(pattern, page_text, re.IGNORECASE))
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.1 <= price_value <= 10000:  # Reasonable price range
                        found_prices.append((pattern, price_value))
                except ValueError:
                    continue
        
        if found_prices:
            print(f"✅ SUCCESS: Found {len(found_prices)} potential prices:")
            for pattern, price in found_prices[:5]:  # Show first 5
                print(f"   - ${price} (pattern: {pattern[:30]}...)")
            return {"success": True, "prices": found_prices}
        
        # Check for keywords that might indicate price locations
        keywords = ['market price', 'nav', 'share price', 'current price', 'last price', 'fund price']
        keyword_mentions = []
        for keyword in keywords:
            matches = list(re.finditer(re.escape(keyword), page_text, re.IGNORECASE))
            keyword_mentions.extend(matches)
        
        dollar_signs = list(re.finditer(r'\$', page_text))
        
        print(f"❌ FAILED: Found {len(keyword_mentions)} price keywords, {len(dollar_signs)} dollar signs")
        
        # Show context around price keywords
        if keyword_mentions:
            print("Price keyword contexts:")
            for i, match in enumerate(keyword_mentions[:3]):
                start = max(0, match.start() - 50)
                end = min(len(page_text), match.end() + 50)
                context = page_text[start:end].replace('\n', ' ').strip()
                print(f"  {i+1}. ...{context}...")
        
        # Show context around dollar signs
        if dollar_signs:
            print("Dollar sign contexts:")
            for i, match in enumerate(dollar_signs[:3]):
                start = max(0, match.start() - 30)
                end = min(len(page_text), match.end() + 30)
                context = page_text[start:end].replace('\n', ' ').strip()
                print(f"  {i+1}. ...{context}...")
        
        # Show some sample content
        print(f"\nSample content (first 800 chars):")
        print(page_text[:800])
        
        return {"success": False, "keyword_mentions": len(keyword_mentions), "dollar_signs": len(dollar_signs)}
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {"success": False, "error": str(e)}
    finally:
        if driver:
            driver.quit()

def main():
    """Test the problematic Franklin Templeton URLs"""
    failing_urls = [
        "https://www.franklintempleton.com/investments/options/exchange-traded-funds/products/39639/SINGLCLASS/franklin-bitcoin-etf/EZBC",
        "https://www.franklintempleton.com/investments/options/exchange-traded-funds/products/40521/SINGLCLASS/franklin-ethereum-etf/EZET",
        "https://www.franklintempleton.com/investments/options/exchange-traded-funds/products/41786/SINGLCLASS/franklin-crypto-index-etf/EZPZ#documents"
    ]
    
    print("🔍 Testing Franklin Templeton ETF URLs...")
    
    results = []
    for i, url in enumerate(failing_urls, 1):
        print(f"\n{i}. Testing Franklin Templeton URL:")
        result = test_franklin_templeton_url(url)
        results.append(result)
    
    print(f"\n{'='*80}")
    print("📊 SUMMARY:")
    print(f"{'='*80}")
    
    success_count = sum(1 for r in results if r.get('success'))
    print(f"Successful extractions: {success_count}/{len(results)}")
    
    for i, result in enumerate(results, 1):
        if result.get('success'):
            print(f"{i}. ✅ SUCCESS - Found {len(result.get('prices', []))} prices")
        else:
            error = result.get('error', 'Unknown error')
            keywords = result.get('keyword_mentions', 0)
            dollars = result.get('dollar_signs', 0)
            print(f"{i}. ❌ FAILED - {error}, {keywords} keywords, {dollars} dollar signs")

if __name__ == "__main__":
    main() 