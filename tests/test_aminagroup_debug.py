#!/usr/bin/env python3
"""
Debug script for Amina Group URLs to understand price extraction
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

def test_aminagroup_url(url):
    """Test a single Amina Group URL to see if we can extract prices"""
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
        print(f"Final URL: {driver.current_url}")
        
        # Look for various price patterns that might be on Amina Group pages
        price_patterns = [
            r'Price.*?(?:USD|CHF|EUR)\s*([\d,\.]+)',     # "Price USD 123.45"
            r'(?:USD|CHF|EUR)\s*([\d,\.]+)',             # "USD 123.45"
            r'Current\s+Price.*?([\d,\.]+)',             # "Current Price 123.45"
            r'Last\s+Price.*?([\d,\.]+)',                # "Last Price 123.45"
            r'Market\s+Price.*?([\d,\.]+)',              # "Market Price 123.45"
            r'Value.*?([\d,\.]+)',                       # "Value 123.45"
            r'NAV.*?([\d,\.]+)',                         # "NAV 123.45"
        ]
        
        found_prices = []
        for pattern in price_patterns:
            matches = list(re.finditer(pattern, page_text, re.IGNORECASE))
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.1 <= price_value <= 10000:  # Reasonable price range for certificates
                        found_prices.append((pattern, price_value))
                except ValueError:
                    continue
        
        # Also look for specific certificate/tracker patterns
        certificate_patterns = [
            r'Certificate\s+Price.*?([\d,\.]+)',
            r'Tracker\s+Price.*?([\d,\.]+)',
            r'Issue\s+Price.*?([\d,\.]+)',
            r'Current\s+Value.*?([\d,\.]+)',
        ]
        
        for pattern in certificate_patterns:
            matches = list(re.finditer(pattern, page_text, re.IGNORECASE))
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.1 <= price_value <= 10000:
                        found_prices.append((pattern, price_value))
                except ValueError:
                    continue
        
        if found_prices:
            print(f"✅ SUCCESS: Found {len(found_prices)} potential prices:")
            for pattern, price in found_prices[:5]:  # Show first 5
                print(f"   - {price} (pattern: {pattern[:40]}...)")
            return {"success": True, "prices": found_prices}
        
        # Check for keywords that might indicate where prices are located
        keywords = ['price', 'value', 'nav', 'current', 'last', 'market', 'certificate', 'tracker']
        keyword_mentions = []
        for keyword in keywords:
            matches = list(re.finditer(re.escape(keyword), page_text, re.IGNORECASE))
            keyword_mentions.extend(matches)
        
        # Look for currency symbols
        currency_symbols = list(re.finditer(r'(USD|CHF|EUR|\$|€)', page_text))
        
        print(f"❌ FAILED: Found {len(keyword_mentions)} price keywords, {len(currency_symbols)} currency mentions")
        
        # Show context around currency symbols
        if currency_symbols:
            print("Currency contexts:")
            for i, match in enumerate(currency_symbols[:3]):
                start = max(0, match.start() - 50)
                end = min(len(page_text), match.end() + 50)
                context = page_text[start:end].replace('\n', ' ').strip()
                print(f"  {i+1}. ...{context}...")
        
        # Show some sample content
        print(f"\nSample content (first 800 chars):")
        print(page_text[:800])
        
        return {"success": False, "keyword_mentions": len(keyword_mentions), "currency_symbols": len(currency_symbols)}
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {"success": False, "error": str(e)}
    finally:
        if driver:
            driver.quit()

def main():
    """Test the problematic Amina Group URLs"""
    failing_urls = [
        "https://aminagroup.com/individuals/investments/eth-usd-tracker-certificate/",
        "https://aminagroup.com/individuals/investments/dot-usd-tracker-certificate/"
    ]
    
    print("🔍 Testing Amina Group URLs...")
    
    results = []
    for i, url in enumerate(failing_urls, 1):
        print(f"\n{i}. Testing Amina Group URL:")
        result = test_aminagroup_url(url)
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
            currencies = result.get('currency_symbols', 0)
            print(f"{i}. ❌ FAILED - {error}, {keywords} keywords, {currencies} currency symbols")

if __name__ == "__main__":
    main() 