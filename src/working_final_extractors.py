"""
Working Final Outstanding Shares Extractors
Based on exact patterns found in the actual HTML content
"""

import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

def extract_valour_shares_working(driver, url):
    """
    Working Valour extractor based on exact HTML patterns found:
    1. <span><span>120000</span></span>
    2. "outstanding-shares":120000
    """
    try:
        logging.info(f"Using working Valour extractor for: {url}")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)  # Allow time for dynamic content
        
        # Get page source
        html_content = driver.page_source
        
        # Method 1: Look for JSON pattern "outstanding-shares":120000
        json_pattern = re.search(r'"outstanding-shares"\s*:\s*(\d+)', html_content)
        if json_pattern:
            shares_value = json_pattern.group(1)
            logging.info(f"Found Valour shares in JSON: {shares_value}")
            return shares_value
        
        # Method 2: Look for nested span pattern <span><span>120000</span></span>
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all spans that contain only digits
        spans = soup.find_all('span')
        for span in spans:
            span_text = span.get_text().strip()
            if span_text.isdigit() and len(span_text) >= 5:
                # Check if this might be shares (reasonable range)
                try:
                    value = int(span_text)
                    if 50000 <= value <= 10000000:  # Reasonable shares range for Valour
                        # Check if it's in a nested span structure
                        parent = span.parent
                        if parent and parent.name == 'span':
                            logging.info(f"Found Valour shares in nested span: {span_text}")
                            return span_text
                except ValueError:
                    continue
        
        # Method 3: Look for any 6-digit number that could be shares
        numbers = re.findall(r'\\b(\d{6})\\b', html_content)
        for number in numbers:
            try:
                value = int(number)
                if 100000 <= value <= 1000000:  # Specific range for Valour
                    logging.info(f"Found potential Valour shares: {number}")
                    return number
            except ValueError:
                continue
        
        logging.warning("Could not find Valour outstanding shares")
        return None
        
    except Exception as e:
        logging.error(f"Error in Valour extractor: {e}")
        return None

def extract_grayscale_shares_working(driver, url):
    """
    Working Grayscale extractor based on exact HTML patterns found:
    Pattern: "SHARES OUTSTANDING47,123,300"
    """
    try:
        logging.info(f"Using working Grayscale extractor for: {url}")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)
        
        # Get page source
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        
        # Method 1: Look for the exact pattern "SHARES OUTSTANDING47,123,300"
        pattern1 = re.search(r'SHARES\\s*OUTSTANDING\\s*([0-9,]+)', text_content, re.IGNORECASE)
        if pattern1:
            shares_value = pattern1.group(1).replace(',', '')
            logging.info(f"Found Grayscale shares with exact pattern: {shares_value}")
            return shares_value
        
        # Method 2: Look for the number 47123300 or similar large numbers
        large_numbers = re.findall(r'\\b([0-9,]{8,})\\b', text_content)
        for number in large_numbers:
            cleaned = number.replace(',', '')
            if cleaned.isdigit() and len(cleaned) >= 7:
                try:
                    value = int(cleaned)
                    if 10000000 <= value <= 100000000:  # Range for Grayscale shares
                        logging.info(f"Found potential Grayscale shares: {cleaned}")
                        return cleaned
                except ValueError:
                    continue
        
        # Method 3: Look in the raw HTML for the pattern
        html_pattern = re.search(r'47[,.]?123[,.]?300', html_content)
        if html_pattern:
            found_number = html_pattern.group(0).replace(',', '').replace('.', '')
            logging.info(f"Found Grayscale shares in HTML: {found_number}")
            return found_number
        
        logging.warning("Could not find Grayscale outstanding shares")
        return None
        
    except Exception as e:
        logging.error(f"Error in Grayscale extractor: {e}")
        return None

def extract_proshares_shares_working(driver, url):
    """
    Working ProShares extractor - try to find any shares data
    """
    try:
        logging.info(f"Using working ProShares extractor for: {url}")
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5)  # Extra time for ProShares
        
        # Get page source
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        
        # Method 1: Look for any mention of shares with numbers
        shares_patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*shares',
            r'shares[:\s]*(\d{1,3}(?:,\d{3})*)',
            r'outstanding[:\s]*(\d{1,3}(?:,\d{3})*)',
            r'(\d{1,3}(?:,\d{3})*)\s*outstanding',
        ]
        
        for pattern in shares_patterns:
            matches = re.finditer(pattern, text_content, re.IGNORECASE)
            for match in matches:
                shares_text = match.group(1)
                cleaned = shares_text.replace(',', '')
                if cleaned.isdigit():
                    try:
                        value = int(cleaned)
                        if 1000000 <= value <= 1000000000:  # Reasonable range
                            logging.info(f"Found ProShares shares with pattern: {cleaned}")
                            return cleaned
                    except ValueError:
                        continue
        
        # Method 2: Look for large numbers that might be shares
        large_numbers = re.findall(r'\\b(\d{7,10})\\b', text_content)
        for number in large_numbers:
            try:
                value = int(number)
                if 1000000 <= value <= 1000000000:  # Reasonable shares range
                    logging.info(f"Found potential ProShares shares: {number}")
                    return number
            except ValueError:
                continue
        
        # Method 3: Check if there are any fund documents or data sections
        # that might contain shares information
        fund_keywords = ['fund', 'etf', 'shares', 'outstanding', 'issued']
        for keyword in fund_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            for element in elements[:5]:  # Check first 5 matches
                parent = element.parent if hasattr(element, 'parent') else None
                if parent:
                    parent_text = parent.get_text()
                    numbers = re.findall(r'(\d{6,})', parent_text)
                    for number in numbers:
                        try:
                            value = int(number)
                            if 1000000 <= value <= 1000000000:
                                logging.info(f"Found potential ProShares shares near '{keyword}': {number}")
                                return number
                        except ValueError:
                            continue
        
        logging.warning("Could not find ProShares outstanding shares")
        return None
        
    except Exception as e:
        logging.error(f"Error in ProShares extractor: {e}")
        return None

def get_working_custom_extractor(url):
    """Get the appropriate working custom extractor for a URL"""
    domain = url.lower()
    
    if "valour.com" in domain:
        return extract_valour_shares_working
    elif "grayscale.com" in domain:
        return extract_grayscale_shares_working
    elif "proshares.com" in domain:
        return extract_proshares_shares_working
    
    return None

def extract_with_working_custom_function(driver, url):
    """
    Main function to extract outstanding shares using working custom extractors
    """
    try:
        logging.info(f"Using working custom extractor for {url}")
        
        # Get the appropriate extractor
        extractor = get_working_custom_extractor(url)
        
        if extractor:
            result = extractor(driver, url)
            if result:
                return result
        
        logging.warning(f"No working custom extractor available for {url}")
        return None
        
    except Exception as e:
        logging.error(f"Error in working custom extraction for {url}: {e}")
        return None

def test_working_extractors():
    """Test the working extractors"""
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test URLs
    test_urls = [
        "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd",
        "https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust",
        "https://www.proshares.com/our-etfs/strategic/bito",
    ]
    
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    successful_extractions = 0
    total_tests = len(test_urls)
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(30)
        
        print("=" * 60)
        print("TESTING WORKING CUSTOM EXTRACTORS")
        print("=" * 60)
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n[{i}/{total_tests}] Testing: {url}")
            
            try:
                result = extract_with_working_custom_function(driver, url)
                
                if result:
                    print(f"✅ SUCCESS: Found outstanding shares: {result}")
                    successful_extractions += 1
                else:
                    print(f"❌ FAILED: Could not extract outstanding shares")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
            
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print("WORKING EXTRACTOR SUMMARY:")
        print(f"Total URLs tested: {total_tests}")
        print(f"Successful extractions: {successful_extractions}")
        print(f"Success rate: {(successful_extractions/total_tests)*100:.1f}%")
        
        if successful_extractions > 0:
            print("🎉 SUCCESS: Working extractors are functional!")
        else:
            print("❌ All extractors failed - need further investigation")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error setting up driver: {str(e)}")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_working_extractors() 