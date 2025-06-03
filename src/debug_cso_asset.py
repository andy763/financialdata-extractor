#!/usr/bin/env python3
"""
Debug script to see exactly what's on the CSO P Asset page
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

def debug_cso_asset():
    """Debug CSO P Asset page to see exact content"""
    
    url = "https://www.csopasset.com/en/products/hk-btcfut#"
    
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
        driver.set_page_load_timeout(60)
        
        print(f"🔍 DEBUGGING CSO P ASSET PAGE")
        print(f"URL: {url}")
        print("=" * 80)
        
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(12)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        
        # Look for all instances of "38" to see if we can find the precise prices
        print("\n📊 All instances of '38' on the page:")
        matches = re.finditer(r'38[\.0-9]*', page_text)
        for i, match in enumerate(matches):
            if i > 10:  # Limit output
                break
            context_start = max(0, match.start() - 100)
            context_end = min(len(page_text), match.end() + 100)
            context = page_text[context_start:context_end].strip()
            print(f"  Found: {match.group()} - Context: ...{context}...")
        
        # Look for all instances of "22" to see what's being picked up
        print("\n📊 All instances of '22' on the page:")
        matches = re.finditer(r'22[\.0-9]*', page_text)
        for i, match in enumerate(matches):
            if i > 10:  # Limit output
                break
            context_start = max(0, match.start() - 100)
            context_end = min(len(page_text), match.end() + 100)
            context = page_text[context_start:context_end].strip()
            print(f"  Found: {match.group()} - Context: ...{context}...")
        
        # Look for "Closing Price" specifically
        print("\n📊 All instances of 'Closing Price':")
        matches = re.finditer(r'Closing\s+Price[^0-9]*([0-9\.]+)', page_text, re.IGNORECASE)
        for match in matches:
            context_start = max(0, match.start() - 50)
            context_end = min(len(page_text), match.end() + 50)
            context = page_text[context_start:context_end].strip()
            print(f"  Found: {match.group(1)} - Context: ...{context}...")
        
        # Save a portion of the page text for manual inspection
        print(f"\n📄 First 2000 characters of page text:")
        print(page_text[:2000])
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    debug_cso_asset() 