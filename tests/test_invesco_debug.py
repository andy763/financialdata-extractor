#!/usr/bin/env python3
"""
Debug script for Invesco ETF pages to understand why price extraction is failing
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

def test_invesco_url(url):
    """Test a single Invesco URL to see what's happening"""
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        
        # Load the page
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)  # Allow for dynamic content
        
        # Check final URL (in case of redirects)
        final_url = driver.current_url
        print(f"Final URL: {final_url}")
        
        # Get page content
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        
        print(f"✅ Page loaded: {len(page_text)} chars")
        
        # Look for various price patterns
        price_patterns = [
            (r'Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Price with currency'),
            (r'Market\s+Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Market Price with currency'),
            (r'NAV[^£$€]*?[£$€]\s*([\d,\.]+)', 'NAV with currency'),
            (r'Current\s+Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Current Price with currency'),
            (r'Last\s+Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Last Price with currency'),
            (r'[£$€]\s*([\d,\.]+)', 'Any currency amount'),
        ]
        
        found_prices = []
        
        for pattern, description in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.1 <= price_value <= 10000:  # Reasonable ETF price range
                        found_prices.append((price_value, description, pattern))
                except ValueError:
                    continue
        
        if found_prices:
            print(f"✅ SUCCESS: Found {len(found_prices)} potential prices:")
            for price, desc, pattern in found_prices[:5]:  # Show first 5
                print(f"   - {price} ({desc})")
            return True
        else:
            print("❌ FAILED: No valid prices found")
            
            # Look for common error indicators
            error_indicators = [
                "404", "not found", "error", "blocked", "access denied", 
                "cookie", "consent", "redirect", "javascript required"
            ]
            
            page_lower = page_text.lower()
            found_indicators = [indicator for indicator in error_indicators if indicator in page_lower]
            
            if found_indicators:
                print(f"🔍 Error indicators found: {found_indicators}")
            
            # Show first 500 chars of page content for debugging
            print(f"📄 Page content preview: {page_text[:500]}...")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    print("🔍 Testing Invesco URLs...")
    
    # URLs from the log that had errors
    test_urls = [
        "https://www.invesco.com/uk/en/financial-products/etfs/invesco-physical-bitcoin.html?msockid=3c4bdec1933068c13047ca3c92f2693e",
        "https://www.invesco.com/uk/en/financial-products/etfs/invesco-coinshares-global-blockchain-ucits-etf-acc.html?msockid=3c4bdec1933068c13047ca3c92f2693e"
    ]
    
    results = []
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. Testing Invesco URL:")
        result = test_invesco_url(url)
        results.append(result)
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 SUMMARY:")
    print(f"{'='*80}")
    successful = sum(results)
    print(f"Successful extractions: {successful}/{len(results)}")
    for i, result in enumerate(results, 1):
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{i}. {status}")

if __name__ == "__main__":
    main() 