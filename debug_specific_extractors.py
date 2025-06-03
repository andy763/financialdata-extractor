#!/usr/bin/env python3
"""
Debug script to test specific extractor issues and develop improved patterns
"""

import time
import logging
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Setup Chrome driver with options"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def debug_grayscale_extractor(driver, url):
    """
    Debug Grayscale extractor for specific test case
    Expected: 47,123,300 for bitcoin-cash-trust
    """
    print(f"\n🔍 DEBUGGING GRAYSCALE: {url}")
    print("Expected: 47,123,300")
    
    try:
        driver.get(url)
        time.sleep(5)
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        
        print(f"✅ Page loaded successfully")
        
        # Method 1: Look for exact pattern "SHARES OUTSTANDING47,123,300"
        pattern1 = re.search(r'SHARES\s*OUTSTANDING\s*([0-9,]+)', text_content, re.IGNORECASE)
        if pattern1:
            shares_value = pattern1.group(1)
            print(f"✅ Method 1 - Found exact pattern: {shares_value}")
            return shares_value
        else:
            print("❌ Method 1 - Exact pattern not found")
        
        # Method 2: Look for any mention of shares outstanding with nearby numbers
        shares_sections = []
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'SHARES OUTSTANDING' in line.upper():
                # Check this line and next few lines for numbers
                context_lines = lines[i:i+5]
                context_text = ' '.join(context_lines)
                numbers = re.findall(r'([0-9,]+)', context_text)
                shares_sections.append({
                    'line': line.strip(),
                    'context': context_text.strip(),
                    'numbers': numbers
                })
        
        if shares_sections:
            print(f"✅ Method 2 - Found {len(shares_sections)} 'SHARES OUTSTANDING' sections:")
            for idx, section in enumerate(shares_sections):
                print(f"  Section {idx+1}:")
                print(f"    Line: {section['line']}")
                print(f"    Numbers found: {section['numbers']}")
                print(f"    Context: {section['context'][:200]}...")
        else:
            print("❌ Method 2 - No 'SHARES OUTSTANDING' sections found")
        
        # Method 3: Look for the specific number 47,123,300 anywhere
        if '47,123,300' in text_content:
            print("✅ Method 3 - Found target number 47,123,300 in page content")
            # Find context around this number
            index = text_content.find('47,123,300')
            context = text_content[max(0, index-100):index+200]
            print(f"  Context: ...{context}...")
        else:
            print("❌ Method 3 - Target number 47,123,300 not found in page")
        
        # Method 4: Search for all large numbers and see what we find
        all_numbers = re.findall(r'([0-9,]+)', text_content)
        large_numbers = [num for num in all_numbers if len(num.replace(',', '')) >= 6]
        print(f"📊 Method 4 - Found {len(large_numbers)} large numbers (6+ digits):")
        for num in large_numbers[:10]:  # Show first 10
            print(f"  {num}")
        
        return None
        
    except Exception as e:
        print(f"❌ Error debugging Grayscale: {e}")
        return None

def debug_vaneck_us_extractor(driver, url):
    """
    Debug VanEck US extractor for specific test case
    Expected: 53,075,000 for bitcoin-etf-hodl
    """
    print(f"\n🔍 DEBUGGING VANECK US: {url}")
    print("Expected: 53,075,000")
    
    try:
        driver.get(url)
        time.sleep(5)
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        
        print(f"✅ Page loaded successfully")
        
        # Method 1: Look for exact pattern "Shares Outstanding53,075,000"
        pattern1 = re.search(r'Shares\s*Outstanding\s*([0-9,]+)', text_content, re.IGNORECASE)
        if pattern1:
            shares_value = pattern1.group(1)
            print(f"✅ Method 1 - Found exact pattern: {shares_value}")
            return shares_value
        else:
            print("❌ Method 1 - Exact pattern not found")
        
        # Method 2: Look for any mention of shares outstanding
        shares_sections = []
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'shares outstanding' in line.lower():
                context_lines = lines[i:i+5]
                context_text = ' '.join(context_lines)
                numbers = re.findall(r'([0-9,]+)', context_text)
                shares_sections.append({
                    'line': line.strip(),
                    'context': context_text.strip(),
                    'numbers': numbers
                })
        
        if shares_sections:
            print(f"✅ Method 2 - Found {len(shares_sections)} 'shares outstanding' sections:")
            for idx, section in enumerate(shares_sections):
                print(f"  Section {idx+1}:")
                print(f"    Line: {section['line']}")
                print(f"    Numbers found: {section['numbers']}")
                print(f"    Context: {section['context'][:200]}...")
        else:
            print("❌ Method 2 - No 'shares outstanding' sections found")
        
        # Method 3: Look for the specific number 53,075,000 anywhere
        if '53,075,000' in text_content:
            print("✅ Method 3 - Found target number 53,075,000 in page content")
            index = text_content.find('53,075,000')
            context = text_content[max(0, index-100):index+200]
            print(f"  Context: ...{context}...")
        else:
            print("❌ Method 3 - Target number 53,075,000 not found in page")
        
        # Method 4: Check if this is the literature page - different content
        if 'literature' in url:
            print("ℹ️  This is a literature page - may have different structure")
        
        # Method 5: Search for all large numbers
        all_numbers = re.findall(r'([0-9,]+)', text_content)
        large_numbers = [num for num in all_numbers if len(num.replace(',', '')) >= 6]
        print(f"📊 Method 5 - Found {len(large_numbers)} large numbers (6+ digits):")
        for num in large_numbers[:10]:
            print(f"  {num}")
        
        return None
        
    except Exception as e:
        print(f"❌ Error debugging VanEck US: {e}")
        return None

def debug_vaneck_de_extractor(driver, url):
    """
    Debug VanEck DE extractor for specific test case  
    Expected: 1,561,000 for polygon-etp
    """
    print(f"\n🔍 DEBUGGING VANECK DE: {url}")
    print("Expected: 1,561,000")
    
    try:
        driver.get(url)
        time.sleep(5)
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        
        print(f"✅ Page loaded successfully")
        
        # Method 1: Look for exact pattern "Notes Outstanding1,561,000"
        pattern1 = re.search(r'Notes\s*Outstanding\s*([0-9,]+)', text_content, re.IGNORECASE)
        if pattern1:
            shares_value = pattern1.group(1)
            print(f"✅ Method 1 - Found exact pattern: {shares_value}")
            return shares_value
        else:
            print("❌ Method 1 - Exact pattern not found")
        
        # Method 2: Look for any mention of notes outstanding
        notes_sections = []
        lines = text_content.split('\n')
        for i, line in enumerate(lines):
            if 'notes outstanding' in line.lower():
                context_lines = lines[i:i+5]
                context_text = ' '.join(context_lines)
                numbers = re.findall(r'([0-9,]+)', context_text)
                notes_sections.append({
                    'line': line.strip(),
                    'context': context_text.strip(),
                    'numbers': numbers
                })
        
        if notes_sections:
            print(f"✅ Method 2 - Found {len(notes_sections)} 'notes outstanding' sections:")
            for idx, section in enumerate(notes_sections):
                print(f"  Section {idx+1}:")
                print(f"    Line: {section['line']}")
                print(f"    Numbers found: {section['numbers']}")
                print(f"    Context: {section['context'][:200]}...")
        else:
            print("❌ Method 2 - No 'notes outstanding' sections found")
        
        # Method 3: Look for the specific number 1,561,000 anywhere
        if '1,561,000' in text_content:
            print("✅ Method 3 - Found target number 1,561,000 in page content")
            index = text_content.find('1,561,000')
            context = text_content[max(0, index-100):index+200]
            print(f"  Context: ...{context}...")
        else:
            print("❌ Method 3 - Target number 1,561,000 not found in page")
        
        # Method 4: Search for all numbers that could be shares/notes
        all_numbers = re.findall(r'([0-9,]+)', text_content)
        medium_numbers = [num for num in all_numbers if 4 <= len(num.replace(',', '')) <= 8]
        print(f"📊 Method 4 - Found {len(medium_numbers)} medium numbers (4-8 digits):")
        for num in medium_numbers[:10]:
            print(f"  {num}")
        
        return None
        
    except Exception as e:
        print(f"❌ Error debugging VanEck DE: {e}")
        return None

def main():
    """Main function to debug all three extractors"""
    print("🔍 DEBUGGING CUSTOM EXTRACTORS - SPECIFIC TEST CASES")
    print("=" * 60)
    
    # Test cases provided by user
    test_cases = [
        {
            'domain': 'grayscale',
            'url': 'https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust',
            'expected': '47,123,300',
            'debug_func': debug_grayscale_extractor
        },
        {
            'domain': 'vaneck_us',
            'url': 'https://www.vaneck.com/us/en/investments/bitcoin-etf-hodl/literature/',
            'expected': '53,075,000',
            'debug_func': debug_vaneck_us_extractor
        },
        {
            'domain': 'vaneck_de',
            'url': 'https://www.vaneck.com/de/en/investments/polygon-etp/overview/',
            'expected': '1,561,000',
            'debug_func': debug_vaneck_de_extractor
        }
    ]
    
    driver = setup_driver()
    
    try:
        for test_case in test_cases:
            print(f"\n🎯 Testing {test_case['domain'].upper()}")
            print(f"URL: {test_case['url']}")
            print(f"Expected: {test_case['expected']}")
            
            result = test_case['debug_func'](driver, test_case['url'])
            
            if result:
                if result == test_case['expected']:
                    print(f"✅ SUCCESS: Found correct value {result}")
                else:
                    print(f"⚠️  MISMATCH: Found {result}, expected {test_case['expected']}")
            else:
                print(f"❌ FAILED: Could not extract shares")
            
            print("-" * 60)
    
    finally:
        driver.quit()
    
    print("\n📋 DEBUGGING COMPLETE")
    print("Use the information above to improve the extractors")

if __name__ == "__main__":
    main()
