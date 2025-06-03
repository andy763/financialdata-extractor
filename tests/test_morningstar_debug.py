#!/usr/bin/env python3
"""
Debug script for Morningstar France fund pages to understand why price extraction is failing
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

def test_morningstar_fr_url(url):
    """Test a single Morningstar France URL to see what's happening"""
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
        print(f"📄 URL appears to be: {'PDF' if 'Format=PDF' in url else 'HTML page'}")
        
        # Check if it's a PDF URL
        if "Format=PDF" in url:
            print("⚠️  WARNING: This URL points to a PDF document, not an HTML page")
            print("   The scraping function is designed for HTML pages, not PDFs")
            return {"success": False, "reason": "PDF URL not supported"}
        
        # Run the same logic as in the main script
        # Method 1: Look for "VL" followed by date and currency amount (most specific)
        vl_patterns = [
            r'VL\d{1,2}/\d{1,2}/\d{4}\s+([A-Z]{3})\s+([\d,\.]+)',  # "VL22/05/2025 EUR 11,19"
            r'VL\s*\d{1,2}/\d{1,2}/\d{4}\s+([A-Z]{3})\s+([\d,\.]+)',  # "VL 22/05/2025 EUR 11,19"
            r'Valeur\s+Liquidative.*?([A-Z]{3})\s+([\d,\.]+)',  # "Valeur Liquidative ... EUR 11,19"
            r'VL.*?([A-Z]{3})\s+([\d,\.]+)',  # "VL ... EUR 11,19"
        ]
        
        found_patterns = []
        for pattern in vl_patterns:
            matches = list(re.finditer(pattern, page_text, re.IGNORECASE))
            for match in matches:
                currency = match.group(1)
                price_str = match.group(2)
                found_patterns.append(f"{currency} {price_str}")
        
        if found_patterns:
            print(f"✅ SUCCESS: Found VL patterns: {found_patterns}")
            # Try to parse the first one
            currency = found_patterns[0].split()[0]
            price_str = found_patterns[0].split()[1]
            
            # Convert European number format
            if ',' in price_str and '.' not in price_str:
                price_normalized = price_str.replace(',', '.')
            elif '.' in price_str and ',' in price_str:
                price_normalized = price_str.replace('.', '').replace(',', '.')
            else:
                price_normalized = price_str
            
            try:
                price_value = float(price_normalized)
                print(f"✅ PARSED PRICE: {currency} {price_value}")
                return {"success": True, "currency": currency, "price": price_value}
            except ValueError:
                print(f"❌ Could not parse price: {price_str}")
        
        # Check for VL mentions
        vl_mentions = list(re.finditer(r'VL|Valeur\s+Liquidative', page_text, re.IGNORECASE))
        currency_matches = list(re.finditer(r'EUR|USD|GBP', page_text))
        
        print(f"❌ FAILED: {len(vl_mentions)} VL mentions, {len(currency_matches)} currency mentions")
        
        if vl_mentions:
            print("VL contexts:")
            for i, match in enumerate(vl_mentions[:3]):
                start = max(0, match.start() - 40)
                end = min(len(page_text), match.end() + 40)
                context = page_text[start:end].replace('\n', ' ').strip()
                print(f"  {i+1}. ...{context}...")
        
        # Show some sample content
        print(f"\nSample content (first 500 chars):")
        print(page_text[:500])
        
        return {"success": False, "vl_mentions": len(vl_mentions), "currency_mentions": len(currency_matches)}
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {"success": False, "error": str(e)}
    finally:
        if driver:
            driver.quit()

def main():
    """Test the problematic Morningstar France URLs"""
    # The actual failing URL from the log
    failing_url = "https://www.morningstar.fr/fr/funds/snapshot/snapshot.aspx?id=F000015OI0&tab=14&DocumentId=2b03657c6feb71b624a4bd4985cedecc&Format=PDF"
    
    # A sample proper Morningstar France fund page (without PDF)
    sample_url = "https://www.morningstar.fr/fr/funds/snapshot/snapshot.aspx?id=F000015OI0"  # Remove the PDF part
    
    print("🔍 Testing Morningstar France URLs...")
    
    print("\n1. Testing the actual failing URL:")
    result1 = test_morningstar_fr_url(failing_url)
    
    print("\n2. Testing without PDF parameter:")
    result2 = test_morningstar_fr_url(sample_url)
    
    print(f"\n{'='*80}")
    print("📊 SUMMARY:")
    print(f"{'='*80}")
    
    print(f"1. Failing URL: {'✅ SUCCESS' if result1.get('success') else '❌ FAILED'}")
    if not result1.get('success'):
        print(f"   Reason: {result1.get('reason', result1.get('error', 'Unknown'))}")
    
    print(f"2. Modified URL: {'✅ SUCCESS' if result2.get('success') else '❌ FAILED'}")
    if result2.get('success'):
        print(f"   Found: {result2.get('currency')} {result2.get('price')}")
    elif not result2.get('success'):
        print(f"   VL mentions: {result2.get('vl_mentions', 0)}, Currency mentions: {result2.get('currency_mentions', 0)}")

if __name__ == "__main__":
    main() 