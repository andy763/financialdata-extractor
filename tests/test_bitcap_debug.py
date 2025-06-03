#!/usr/bin/env python3
"""
Debug script for Bitcap URLs to understand and resolve redirect issues
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

def test_bitcap_url(url):
    """Test a single Bitcap URL to understand redirect behavior"""
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
        print(f"Loading URL: {url}")
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Check where we ended up after redirects
        final_url = driver.current_url
        print(f"Final URL after redirects: {final_url}")
        
        # Wait for JavaScript to load
        time.sleep(8)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        
        print(f"✅ Page loaded: {len(page_text)} chars")
        
        # Check if this is a popup/redirect page
        if "pop-up" in final_url.lower():
            print("⚠️  WARNING: URL redirected to a popup page")
            print("   Attempting to find the actual fund page...")
            
            # Look for links to the actual fund pages
            fund_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                link_text = link.get_text(strip=True)
                if href and any(keyword in href.lower() for keyword in ['fund', 'product', 'opportunities', 'crypto']):
                    if 'pop-up' not in href.lower():
                        fund_links.append((href, link_text))
            
            if fund_links:
                print(f"Found {len(fund_links)} potential fund links:")
                for href, text in fund_links[:3]:
                    print(f"  - {text}: {href}")
                
                # Try the first promising link
                best_link = fund_links[0][0]
                if not best_link.startswith('http'):
                    if best_link.startswith('/'):
                        best_link = 'https://bitcap.com' + best_link
                    else:
                        best_link = 'https://bitcap.com/' + best_link
                
                print(f"\nTrying redirect to: {best_link}")
                driver.get(best_link)
                time.sleep(5)
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                page_text = soup.get_text(" ", strip=True)
                final_url = driver.current_url
                print(f"New final URL: {final_url}")
        
        # Look for share price patterns
        share_price_patterns = [
            r'Share price\s*€\s*([\d,\.]+)',           # "Share price €81.28"
            r'Share price.*?€\s*([\d,\.]+)',           # "Share price [anything] €81.28"
            r'€\s*([\d,\.]+).*?share price',           # "€81.28 [anything] share price"
            r'price\s*€\s*([\d,\.]+)',                 # "price €81.28"
            r'value\s*€\s*([\d,\.]+)',                 # "value €81.28"
            r'net asset value\s*€\s*([\d,\.]+)',       # "net asset value €81.28"
        ]
        
        found_prices = []
        for pattern in share_price_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                try:
                    price_value = float(price_str.replace(',', '.'))
                    if 0.01 <= price_value <= 10000:  # Reasonable price range
                        found_prices.append((pattern, price_value))
                except ValueError:
                    continue
        
        if found_prices:
            print(f"✅ SUCCESS: Found {len(found_prices)} potential prices:")
            for pattern, price in found_prices[:5]:
                print(f"   - €{price} (pattern: {pattern[:30]}...)")
            return {"success": True, "prices": found_prices, "final_url": final_url}
        
        # Check for any Euro amounts on the page
        euro_amounts = re.findall(r'€\s*([\d,\.]+)', page_text)
        print(f"Found {len(euro_amounts)} Euro amounts on page: {euro_amounts[:10]}")
        
        # Check for fund-related keywords
        fund_keywords = ['fund', 'share', 'price', 'value', 'nav', 'asset']
        keyword_count = sum(1 for keyword in fund_keywords if keyword.lower() in page_text.lower())
        print(f"Found {keyword_count}/{len(fund_keywords)} fund-related keywords")
        
        # Show some sample content
        print(f"\nSample content (first 500 chars):")
        print(page_text[:500])
        
        return {"success": False, "euro_amounts": len(euro_amounts), "keyword_count": keyword_count, "final_url": final_url}
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {"success": False, "error": str(e)}
    finally:
        if driver:
            driver.quit()

def main():
    """Test the problematic Bitcap URLs"""
    failing_urls = [
        "https://bitcap.com/en/bit-crypto-opportunities-institutional-en/?confirmed=1",
        "https://bitcap.com/en/global-leaders-ucits-professional-en/"
    ]
    
    print("🔍 Testing Bitcap URLs...")
    
    results = []
    for i, url in enumerate(failing_urls, 1):
        print(f"\n{i}. Testing Bitcap URL:")
        result = test_bitcap_url(url)
        results.append(result)
    
    print(f"\n{'='*80}")
    print("📊 SUMMARY:")
    print(f"{'='*80}")
    
    success_count = sum(1 for r in results if r.get('success'))
    print(f"Successful extractions: {success_count}/{len(results)}")
    
    for i, result in enumerate(results, 1):
        if result.get('success'):
            print(f"{i}. ✅ SUCCESS - Found {len(result.get('prices', []))} prices")
            print(f"   Final URL: {result.get('final_url', 'Unknown')}")
        else:
            error = result.get('error', 'Unknown error')
            euros = result.get('euro_amounts', 0)
            keywords = result.get('keyword_count', 0)
            final_url = result.get('final_url', 'Unknown')
            print(f"{i}. ❌ FAILED - {error}")
            print(f"   Euro amounts: {euros}, Keywords: {keywords}")
            print(f"   Final URL: {final_url}")

if __name__ == "__main__":
    main() 