#!/usr/bin/env python3
"""
Test script to verify the enhanced validation system works with real problematic URLs
Tests against actual URLs that were causing .0 errors in the most recent run
"""

import sys
import os
import time
import logging

# Add the main directory to path so we can import functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import is_valid_share_price, analyze_website_with_groq, GROQ_AVAILABLE
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re

def test_real_problematic_urls():
    """Test the enhanced validation against real URLs that were causing problems"""
    
    print("🔍 TESTING REAL PROBLEMATIC URLS")
    print("=" * 60)
    
    # URLs from the log file that were causing .0 errors
    test_urls = [
        {
            "url": "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
            "expected_real_price": 23.15,  # From our web search
            "description": "WisdomTree Physical Bitcoin - was returning .0 errors"
        },
        {
            "url": "https://www.calamos.com/funds/etf/calamos-bitcoin-structured-alt-protection-etf-january-cboj/",
            "expected_real_price": 25.46,  # From our web search  
            "description": "Calamos CBOJ - was returning .0 errors"
        }
    ]
    
    # Test with simple requests (lightweight test)
    print("\n📡 TESTING WITH SIMPLE HTTP REQUESTS")
    print("-" * 50)
    
    for i, test in enumerate(test_urls, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"URL: {test['url']}")
        print(f"Expected real price: ${test['expected_real_price']}")
        
        try:
            # Make a simple request to get the page content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(test['url'], headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                page_text = soup.get_text(' ', strip=True)
                
                # Look for numbers that might be mistaken for prices
                import re
                numbers = re.findall(r'\b\d{1,4}(?:\.\d{1,2})?\b', page_text)
                
                print(f"Found {len(numbers)} potential numbers in page")
                
                # Test our validation on some found numbers
                problematic_numbers = []
                valid_numbers = []
                
                for num_str in numbers[:20]:  # Test first 20 numbers found
                    try:
                        num = float(num_str)
                        if is_valid_share_price(num, page_text[:1000], test['url']):
                            valid_numbers.append(num)
                        else:
                            problematic_numbers.append(num)
                    except ValueError:
                        continue
                
                print(f"✅ Valid prices detected: {len(valid_numbers)} numbers")
                print(f"❌ Invalid prices filtered: {len(problematic_numbers)} numbers")
                
                if valid_numbers:
                    print(f"Valid prices found: {valid_numbers[:5]}")
                if problematic_numbers:
                    print(f"Filtered out: {problematic_numbers[:10]}")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test with AI if available
    if GROQ_AVAILABLE:
        print(f"\n🤖 TESTING WITH AI ANALYSIS")
        print("-" * 50)
        
        for i, test in enumerate(test_urls, 1):
            print(f"\nAI Test {i}: {test['description']}")
            
            try:
                # Use our AI analysis function
                response = requests.get(test['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                if response.status_code == 200:
                    result = analyze_website_with_groq(response.content, test['url'])
                    
                    if "ai_extracted_price" in result:
                        ai_price = result["ai_extracted_price"]
                        print(f"🤖 AI extracted: ${ai_price}")
                        
                        # Check if AI price is close to expected
                        expected = test['expected_real_price']
                        difference = abs(ai_price - expected) / expected * 100
                        
                        if difference < 5:  # Within 5%
                            print(f"✅ AI result accurate! (within {difference:.1f}% of expected)")
                        else:
                            print(f"⚠️  AI result differs by {difference:.1f}% from expected")
                            
                        # Test our validation on the AI result
                        if is_valid_share_price(ai_price, str(result), test['url']):
                            print(f"✅ AI price passed validation")
                        else:
                            print(f"❌ AI price failed validation")
                    else:
                        print(f"❌ AI analysis failed: {result.get('error', 'Unknown error')}")
                else:
                    print(f"❌ Could not fetch page for AI analysis")
                    
            except Exception as e:
                print(f"❌ AI test error: {e}")
    else:
        print(f"\n🤖 AI ANALYSIS SKIPPED (Groq not available)")

def test_validation_improvements():
    """Test specific improvements we made to validation"""
    
    print(f"\n🔧 TESTING VALIDATION IMPROVEMENTS")
    print("=" * 60)
    
    # Test cases showing before/after our improvements
    improvement_tests = [
        {
            "value": 25.0,
            "context": "Current market price trading price",
            "url": "https://example.com/crypto-etf",
            "description": "Whole number with price context - should now PASS"
        },
        {
            "value": 80.0,
            "context": "80% protection level downside",
            "url": "https://calamos.com/bitcoin-etf",
            "description": "Protection percentage - should FAIL"
        },
        {
            "value": 0.75,
            "context": "Expense ratio 0.75% TER fee",
            "url": "https://example.com/etf",
            "description": "Expense ratio with context - should FAIL"
        },
        {
            "value": 0.75,
            "context": "Share price market price current",
            "url": "https://example.com/stock",
            "description": "Small decimal with price context - should PASS"
        }
    ]
    
    for i, test in enumerate(improvement_tests, 1):
        result = is_valid_share_price(test['value'], test['context'], test['url'])
        status = "✅ PASS" if result else "❌ REJECT"
        
        print(f"\nImprovement Test {i}: {status}")
        print(f"  Value: {test['value']}")
        print(f"  Context: {test['context']}")
        print(f"  Description: {test['description']}")

def investigate_betashares(driver, url):
    """
    Detailed investigation of BetaShares to find the most accurate price
    """
    print(f"\n🔍 DETAILED INVESTIGATION: BetaShares")
    print(f"URL: {url}")
    
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(12)  # Extra time for dynamic content
    except Exception:
        print("❌ Page load timeout")
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    print("\n📊 All dollar amounts found on page:")
    dollar_matches = re.finditer(r'\$\s*([\d,\.]+)', page_text, re.IGNORECASE)
    prices_found = []
    
    for i, match in enumerate(dollar_matches):
        if i > 20:  # Limit output
            break
        price_str = match.group(1)
        try:
            price_value = float(price_str.replace(',', ''))
            context_start = max(0, match.start() - 50)
            context_end = min(len(page_text), match.end() + 50)
            context = page_text[context_start:context_end].strip()
            
            print(f"  ${price_value} - Context: ...{context}...")
            prices_found.append((price_value, context))
        except ValueError:
            continue
    
    # Look for the most likely price candidates
    print("\n🎯 Most likely price candidates:")
    for price, context in prices_found:
        if 1 <= price <= 100:  # Reasonable ETF price range
            if any(keyword in context.lower() for keyword in ['price', 'nav', 'unit', 'market', 'current', 'last']):
                print(f"  ✅ ${price} - {context}")

def investigate_csopasset(driver, url):
    """
    Detailed investigation of CSO P Asset to find the actual price
    """
    print(f"\n🔍 DETAILED INVESTIGATION: CSO P Asset")
    print(f"URL: {url}")
    
    driver.get(url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(12)  # Extra time for dynamic content
    except Exception:
        print("❌ Page load timeout")
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    
    print("\n📊 All price-like patterns found on page:")
    
    # Look for various currency patterns
    patterns = [
        (r'HK\$\s*([\d,\.]+)', 'HK Dollar'),
        (r'\$\s*([\d,\.]+)', 'Dollar'),
        (r'USD\s*([\d,\.]+)', 'USD'),
        (r'([\d,\.]+)\s*HKD', 'HKD'),
        (r'([\d,\.]+)\s*USD', 'USD suffix'),
        (r'Price[^0-9]*?([\d,\.]+)', 'Price context'),
        (r'NAV[^0-9]*?([\d,\.]+)', 'NAV context'),
    ]
    
    for pattern, desc in patterns:
        matches = re.finditer(pattern, page_text, re.IGNORECASE)
        for match in matches:
            price_str = match.group(1)
            try:
                price_value = float(price_str.replace(',', ''))
                if 0.1 <= price_value <= 10000:  # Reasonable range
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(page_text), match.end() + 50)
                    context = page_text[context_start:context_end].strip()
                    print(f"  {desc}: {price_value} - Context: ...{context}...")
            except ValueError:
                continue

def create_improved_functions():
    """Create improved functions based on investigation results"""
    
    # URLs to investigate
    test_urls = [
        ("https://www.betashares.com.au/fund/crypto-innovators-etf/#resources", investigate_betashares),
        ("https://www.csopasset.com/en/products/hk-btcfut#", investigate_csopasset),
    ]
    
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
        
        print("🔬 DETAILED INVESTIGATION OF REMAINING PROBLEMATIC URLS")
        print("=" * 80)
        
        for url, func in test_urls:
            func(driver, url)
                
    except Exception as e:
        print(f"Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("🧪 COMPREHENSIVE VALIDATION TESTING")
    print("="*80)
    
    test_real_problematic_urls()
    test_validation_improvements()
    
    print(f"\n🎯 TESTING COMPLETE!")
    print(f"The enhanced validation system should now significantly reduce .0 errors")
    print(f"while correctly accepting valid share prices!")
    
    create_improved_functions() 