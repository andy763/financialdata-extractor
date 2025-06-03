#!/usr/bin/env python3
"""
Simple debug script for one Grayscale fund page
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

def test_grayscale_simple():
    """Test one Grayscale URL"""
    url = "https://www.grayscale.com/funds/grayscale-chainlink-trust"
    
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
        driver.set_page_load_timeout(30)
        
        # Load the page
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Wait for JavaScript to load
        time.sleep(8)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        
        print(f"✅ Page loaded successfully")
        print(f"📄 Page text length: {len(page_text)} characters")
        
        # Search for Market Price patterns
        pattern1 = re.search(
            r'Market Price\s+as\s+of\s+\d{1,2}/\d{1,2}/\d{4}\s*\$\s*([\d,\.]+)', 
            page_text, re.IGNORECASE
        )
        
        if pattern1:
            print(f"✅ FOUND Market Price: ${pattern1.group(1)}")
            return True
        else:
            print("❌ Market Price pattern NOT found")
        
        # Search for any mention of "Market Price"
        market_price_matches = list(re.finditer(r'market\s+price', page_text, re.IGNORECASE))
        print(f"📊 Found {len(market_price_matches)} 'Market Price' mentions")
        
        # Search for any dollar amounts
        dollar_matches = list(re.finditer(r'\$\s*([\d,\.]+)', page_text))
        print(f"💰 Found {len(dollar_matches)} dollar amounts")
        
        if dollar_matches:
            print("First 5 dollar amounts:")
            for i, match in enumerate(dollar_matches[:5]):
                start = max(0, match.start() - 20)
                end = min(len(page_text), match.end() + 20)
                context = page_text[start:end].replace('\n', ' ').strip()
                print(f"  ${match.group(1)} in: ...{context}...")
        
        # Check page title
        title = soup.find('title')
        if title:
            print(f"🏷️ Page title: {title.get_text(strip=True)}")
        
        # Save first part of page for analysis
        print(f"\n📝 First 500 characters:")
        print(page_text[:500])
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_grayscale_simple() 