#!/usr/bin/env python3
"""
Test script to verify QR Asset COTA price extraction
Tests the custom function against the example URL provided
"""

import sys
import os
import time

# Add the main directory to path so we can import functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import get_qrasset_cota_price, fetch_and_extract_data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def test_qrasset_extraction():
    """Test the QR Asset COTA extraction with the example URL"""
    
    print("🇧🇷 TESTING QR ASSET COTA EXTRACTION")
    print("=" * 60)
    
    test_url = "https://qrasset.com.br/qbtc11/#cesta"
    expected_pattern = "R$ 38,09"  # Example from user
    
    print(f"Test URL: {test_url}")
    print(f"Expected pattern: COTA EM [date] {expected_pattern}")
    print(f"Expected value: 38.09 (converted to float)")
    
    # Setup Selenium driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu") 
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        
        print(f"\n🔍 Testing custom QR Asset function...")
        
        # Test the custom function
        try:
            price = get_qrasset_cota_price(driver, test_url)
            print(f"✅ SUCCESS: Custom function extracted price: R$ {price}")
            
            # Validate the result
            if 30.0 <= price <= 50.0:  # Reasonable range around 38.09
                print(f"✅ Price validation: Value {price} is in reasonable range")
            else:
                print(f"⚠️  Price validation: Value {price} seems outside expected range")
                
        except Exception as e:
            print(f"❌ FAILED: Custom function error: {e}")
        
        print(f"\n🔧 Testing integrated extraction...")
        
        # Test the integrated extraction function
        try:
            keywords = ["valor da cota", "cota", "price"]
            result = fetch_and_extract_data(driver, test_url, keywords)
            print(f"✅ SUCCESS: Integrated function result: {result}")
            
            if "valor da cota" in result:
                integrated_price = result["valor da cota"]
                print(f"✅ Extracted 'valor da cota': R$ {integrated_price}")
                
                # Compare with custom function result if both worked
                if 'price' in locals():
                    if abs(price - integrated_price) < 0.01:
                        print(f"✅ Consistency check: Both methods returned same value")
                    else:
                        print(f"⚠️  Consistency check: Methods returned different values")
            else:
                print(f"⚠️  No 'valor da cota' found in result")
                
        except Exception as e:
            print(f"❌ FAILED: Integrated function error: {e}")
            
        print(f"\n📊 ADDITIONAL DEBUGGING")
        print("-" * 40)
        
        # Get page content for debugging
        try:
            driver.get(test_url)
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(5)
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            page_text = soup.get_text(" ", strip=True)
            
            # Look for COTA patterns
            import re
            cota_matches = re.findall(r'COTA[^R]*R\$\s*[\d,\.]+', page_text, re.IGNORECASE)
            if cota_matches:
                print(f"Found COTA patterns:")
                for match in cota_matches[:3]:
                    print(f"  - {match}")
            else:
                print(f"❌ No COTA patterns found in page text")
                
            # Look for any R$ patterns
            real_matches = re.findall(r'R\$\s*[\d,\.]+', page_text)
            if real_matches:
                print(f"Found R$ patterns:")
                for match in real_matches[:5]:
                    print(f"  - {match}")
            else:
                print(f"❌ No R$ patterns found in page text")
                
        except Exception as e:
            print(f"❌ Debugging error: {e}")
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_qrasset_extraction() 