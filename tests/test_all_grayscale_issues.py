#!/usr/bin/env python3
"""
Test all the failing Grayscale URLs from the log
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

def test_grayscale_url(url):
    """Test a single Grayscale URL"""
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
        time.sleep(10)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        
        print(f"✅ Page loaded: {len(page_text)} chars")
        
        # Run the same logic as in the main script
        # Method 1: Look for "Market Price as of MM/DD/YYYY $XX.XX" pattern (MOST RELIABLE)
        pattern1 = re.search(
            r'Market Price\s+as\s+of\s+\d{1,2}/\d{1,2}/\d{4}\s*\$\s*([\d,\.]+)', 
            page_text, re.IGNORECASE
        )
        if pattern1:
            price_str = pattern1.group(1)
            price_normalized = price_str.replace(',', '')
            try:
                price = float(price_normalized)
                print(f"✅ SUCCESS Method 1: Market Price ${price}")
                return {"success": True, "method": 1, "price": price}
            except ValueError:
                print(f"❌ Method 1: Could not parse price '{price_str}'")
        
        # Method 2: Look for price before "Market Price as of" pattern 
        pattern2 = re.search(
            r'\$\s*([\d,\.]+)\s+Market Price\s+as\s+of\s+\d{1,2}/\d{1,2}/\d{4}', 
            page_text, re.IGNORECASE
        )
        if pattern2:
            price_str = pattern2.group(1)
            price_normalized = price_str.replace(',', '')
            try:
                price = float(price_normalized)
                print(f"✅ SUCCESS Method 2: Market Price ${price}")
                return {"success": True, "method": 2, "price": price}
            except ValueError:
                print(f"❌ Method 2: Could not parse price '{price_str}'")
        
        # Method 3: Look for flexible "Market Price" and "as of" with price nearby
        pattern3 = re.search(
            r'Market Price.*?as\s+of.*?\$\s*([\d,\.]+)', 
            page_text, re.IGNORECASE | re.DOTALL
        )
        if pattern3:
            price_str = pattern3.group(1)
            price_normalized = price_str.replace(',', '')
            try:
                price_value = float(price_normalized)
                if price_value < 10000:  # Reasonable fund price range
                    print(f"✅ SUCCESS Method 3: Market Price ${price_value}")
                    return {"success": True, "method": 3, "price": price_value}
                else:
                    print(f"⚠️ Method 3: Price ${price_value} too large, continuing...")
            except ValueError:
                print(f"❌ Method 3: Could not parse price '{price_str}'")
        
        # Check for Market Price mentions
        market_price_matches = list(re.finditer(r'market\s+price', page_text, re.IGNORECASE))
        dollar_matches = list(re.finditer(r'\$\s*([\d,\.]+)', page_text))
        
        print(f"❌ FAILED: {len(market_price_matches)} 'Market Price' mentions, {len(dollar_matches)} dollar amounts")
        
        if market_price_matches:
            print("Market Price contexts:")
            for i, match in enumerate(market_price_matches[:3]):
                start = max(0, match.start() - 40)
                end = min(len(page_text), match.end() + 40)
                context = page_text[start:end].replace('\n', ' ').strip()
                print(f"  {i+1}. ...{context}...")
        
        return {"success": False, "market_price_mentions": len(market_price_matches), "dollar_amounts": len(dollar_matches)}
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {"success": False, "error": str(e)}
    finally:
        if driver:
            driver.quit()

def main():
    """Test all failing Grayscale URLs from the log"""
    failing_urls = [
        "https://www.grayscale.com/funds/grayscale-chainlink-trust",
        "https://www.grayscale.com/funds/grayscale-digital-large-cap-fund",
        "https://www.grayscale.com/funds/grayscale-filecoin-trust",
        "https://www.grayscale.com/funds/grayscale-horizen-trust",
        "https://www.grayscale.com/funds/grayscale-litecoin-trust"
    ]
    
    print("🔍 Testing all failing Grayscale URLs...")
    results = {}
    
    for url in failing_urls:
        result = test_grayscale_url(url)
        results[url] = result
        time.sleep(2)  # Small delay between requests
    
    print(f"\n{'='*80}")
    print("📊 SUMMARY:")
    print(f"{'='*80}")
    
    successful = 0
    failed = 0
    
    for url, result in results.items():
        if result["success"]:
            successful += 1
            method = result["method"]
            price = result["price"]
            print(f"✅ {url}")
            print(f"   Method {method}, Price: ${price}")
        else:
            failed += 1
            print(f"❌ {url}")
            if "error" in result:
                print(f"   Error: {result['error']}")
            else:
                mentions = result.get("market_price_mentions", 0)
                dollars = result.get("dollar_amounts", 0)
                print(f"   {mentions} market price mentions, {dollars} dollar amounts")
    
    print(f"\n📈 RESULTS: {successful} successful, {failed} failed out of {len(failing_urls)} total")

if __name__ == "__main__":
    main() 