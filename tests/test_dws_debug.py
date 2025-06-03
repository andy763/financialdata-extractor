#!/usr/bin/env python3
"""
Debug script for DWS ETF pages to understand why price extraction is failing
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

def test_dws_url(url):
    """Test a single DWS URL to see what's happening"""
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
        
        # Look for various price patterns relevant to DWS/Xtrackers
        price_patterns = [
            (r'Value per ETC security[^0-9]*?([\d,\.]+)\s*USD', 'Value per ETC security USD'),
            (r'Value per ETC security.*?([\d,\.]+)', 'Value per ETC security (any)'),
            (r'Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Price with currency'),
            (r'Market\s+Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Market Price with currency'),
            (r'NAV[^£$€]*?[£$€]\s*([\d,\.]+)', 'NAV with currency'),
            (r'Current\s+Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Current Price with currency'),
            (r'Last\s+Price[^£$€]*?[£$€]\s*([\d,\.]+)', 'Last Price with currency'),
            (r'[£$€]\s*([\d,\.]+)', 'Any currency amount'),
            (r'([\d,\.]+)\s*USD', 'Any USD amount'),
        ]
        
        found_prices = []
        
        for pattern, description in price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', ''))
                    if 0.1 <= price_value <= 100000:  # Reasonable ETC price range
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
            
            # Check if this is an Xtrackers Galaxy page specifically
            if "xtrackers galaxy" in page_text.lower():
                print("🔍 This is an Xtrackers Galaxy page - checking for existing logic")
                
                # Test the existing logic from the main script
                text = page_text
                m = re.search(r"Value per ETC security.*?([\d\.,]+)\s*USD", text, re.IGNORECASE)
                if m:
                    raw_val = m.group(1)
                    print(f"🔍 Found raw value with existing logic: {raw_val}")
                    
                    # Test normalization logic
                    if "," in raw_val and "." in raw_val:
                        norm = raw_val.replace(".", "").replace(",", ".")
                    elif "," in raw_val:
                        norm = raw_val.replace(",", ".")
                    else:
                        norm = raw_val.replace(",", "")
                    
                    print(f"🔍 Normalized value: {norm}")
                    
                    try:
                        price_val = float(norm)
                        print(f"✅ Existing logic would extract: {price_val}")
                        return True
                    except ValueError:
                        print(f"❌ Could not parse '{norm}' as float")
            
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
    print("🔍 Testing DWS ETF URLs...")
    
    # URLs from the log that had errors
    test_urls = [
        "https://etf.dws.com/en-ch/etc/CH1315732250-xtrackers-galaxy-physical-bitcoin-etc-securities/",
        "https://etf.dws.com/en-fi/etc/CH1315732268-xtrackers-galaxy-physical-ethereum-etc-securities/"
    ]
    
    results = []
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. Testing DWS URL:")
        result = test_dws_url(url)
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