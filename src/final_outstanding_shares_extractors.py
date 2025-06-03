"""
Final Outstanding Shares Extractors Based on Actual Website Structure Analysis
This addresses the specific patterns found in the debugging phase
"""

import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

def extract_valour_shares_final(driver, url):
    """
    Final Valour extractor based on actual structure analysis
    Found pattern: "Outstanding Shares120000" and JSON data
    """
    try:
        logging.info(f"Using final Valour extractor for: {url}")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)
        
        # Get page source and parse
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Method 1: Look for the exact pattern found in debugging
        text_content = soup.get_text()
        
        # Pattern: "Outstanding Shares120000"
        pattern1 = re.search(r'Outstanding\s*Shares\s*(\d+)', text_content, re.IGNORECASE)
        if pattern1:
            shares_value = pattern1.group(1)
            logging.info(f"Found Valour shares with pattern 1: {shares_value}")
            return shares_value
        
        # Method 2: Look for JSON data with outstanding-shares
        json_pattern = re.search(r'"outstanding-shares"\s*:\s*(\d+)', html_content)
        if json_pattern:
            shares_value = json_pattern.group(1)
            logging.info(f"Found Valour shares in JSON: {shares_value}")
            return shares_value
        
        # Method 3: Look for span elements with large numbers
        spans = soup.find_all('span')
        for span in spans:
            span_text = span.get_text().strip()
            if span_text.isdigit() and len(span_text) >= 5:
                # Check if this might be shares (reasonable range)
                try:
                    value = int(span_text)
                    if 10000 <= value <= 100000000:  # Reasonable shares range
                        logging.info(f"Found potential Valour shares in span: {span_text}")
                        return span_text
                except ValueError:
                    continue
        
        logging.warning("Could not find Valour outstanding shares")
        return None
        
    except Exception as e:
        logging.error(f"Error in Valour extractor: {e}")
        return None

def extract_grayscale_shares_final(driver, url):
    """
    Final Grayscale extractor based on actual structure analysis
    Found pattern: "SHARES OUTSTANDING47,123,300"
    """
    try:
        logging.info(f"Using final Grayscale extractor for: {url}")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)
        
        # Get page source and parse
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        
        # Method 1: Look for the exact pattern found in debugging
        # Pattern: "SHARES OUTSTANDING47,123,300"
        pattern1 = re.search(r'SHARES\s*OUTSTANDING\s*([0-9,]+)', text_content, re.IGNORECASE)
        if pattern1:
            shares_value = pattern1.group(1).replace(',', '')
            logging.info(f"Found Grayscale shares with pattern 1: {shares_value}")
            return shares_value
        
        # Method 2: Alternative patterns
        patterns = [
            r'outstanding\s*shares?\s*[:\s]*([0-9,.\s]+)',
            r'shares?\s*outstanding\s*[:\s]*([0-9,.\s]+)',
            r'([0-9,]+)\s*shares?\s*outstanding',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                shares_text = match.group(1).strip()
                # Clean the number
                cleaned = re.sub(r'[^\d]', '', shares_text)
                if cleaned and len(cleaned) >= 6:
                    logging.info(f"Found Grayscale shares with pattern: {cleaned}")
                    return cleaned
        
        # Method 3: Look for elements with shares-related classes
        shares_elements = soup.select('[class*="shares"]')
        for elem in shares_elements:
            elem_text = elem.get_text().strip()
            number_match = re.search(r'([0-9,]+)', elem_text)
            if number_match:
                number = number_match.group(1).replace(',', '')
                if len(number) >= 6:
                    logging.info(f"Found Grayscale shares in shares element: {number}")
                    return number
        
        logging.warning("Could not find Grayscale outstanding shares")
        return None
        
    except Exception as e:
        logging.error(f"Error in Grayscale extractor: {e}")
        return None

def extract_proshares_shares_final(driver, url):
    """
    Final ProShares extractor - need to investigate further
    The debugging showed tables but no clear shares pattern
    """
    try:
        logging.info(f"Using final ProShares extractor for: {url}")
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)
        
        # Get page source and parse
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Method 1: Look for holdings/portfolio tables
        tables = soup.find_all('table')
        for table in tables:
            # Look for table headers that might indicate shares data
            headers = table.find_all(['th', 'td'])
            header_text = ' '.join([h.get_text().strip().lower() for h in headers])
            
            if any(keyword in header_text for keyword in ['shares', 'outstanding', 'contracts']):
                # Look for data in this table
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    row_text = ' '.join([cell.get_text().strip() for cell in cells])
                    
                    # Look for large numbers that might be shares
                    numbers = re.findall(r'([0-9,]+)', row_text)
                    for number in numbers:
                        cleaned = number.replace(',', '')
                        if cleaned.isdigit() and len(cleaned) >= 6:
                            try:
                                value = int(cleaned)
                                if 1000000 <= value <= 1000000000:  # Reasonable range
                                    logging.info(f"Found potential ProShares shares in table: {cleaned}")
                                    return cleaned
                            except ValueError:
                                continue
        
        # Method 2: Look for any large numbers in the page that might be shares
        text_content = soup.get_text()
        
        # Look for patterns like "X shares outstanding" or similar
        patterns = [
            r'(\d{6,})\s*shares?\s*outstanding',
            r'outstanding\s*shares?\s*[:\s]*(\d{6,})',
            r'shares?\s*outstanding\s*[:\s]*(\d{6,})',
            r'total\s*shares?\s*[:\s]*(\d{6,})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                shares_value = match.group(1)
                logging.info(f"Found ProShares shares with text pattern: {shares_value}")
                return shares_value
        
        # Method 3: Look for specific fund data sections
        # ProShares might have fund data in specific divs or sections
        fund_sections = soup.find_all(['div', 'section'], class_=re.compile(r'fund|data|info|details', re.I))
        for section in fund_sections:
            section_text = section.get_text()
            numbers = re.findall(r'(\d{6,})', section_text)
            for number in numbers:
                try:
                    value = int(number)
                    if 1000000 <= value <= 1000000000:  # Reasonable shares range
                        logging.info(f"Found potential ProShares shares in fund section: {number}")
                        return number
                except ValueError:
                    continue
        
        logging.warning("Could not find ProShares outstanding shares")
        return None
        
    except Exception as e:
        logging.error(f"Error in ProShares extractor: {e}")
        return None

def get_final_custom_extractor(url):
    """Get the appropriate final custom extractor for a URL"""
    domain = url.lower()
    
    if "valour.com" in domain:
        return extract_valour_shares_final
    elif "grayscale.com" in domain:
        return extract_grayscale_shares_final
    elif "proshares.com" in domain:
        return extract_proshares_shares_final
    
    return None

def extract_with_final_custom_function(driver, url):
    """
    Main function to extract outstanding shares using final custom extractors
    """
    try:
        logging.info(f"Using final custom extractor for {url}")
        
        # Get the appropriate extractor
        extractor = get_final_custom_extractor(url)
        
        if extractor:
            result = extractor(driver, url)
            if result:
                return result
        
        logging.warning(f"No final custom extractor available for {url}")
        return None
        
    except Exception as e:
        logging.error(f"Error in final custom extraction for {url}: {e}")
        return None

def test_final_extractors():
    """Test the final extractors"""
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
        print("TESTING FINAL CUSTOM EXTRACTORS")
        print("=" * 60)
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n[{i}/{total_tests}] Testing: {url}")
            
            try:
                result = extract_with_final_custom_function(driver, url)
                
                if result:
                    print(f"✅ SUCCESS: Found outstanding shares: {result}")
                    successful_extractions += 1
                else:
                    print(f"❌ FAILED: Could not extract outstanding shares")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
            
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print("FINAL EXTRACTOR SUMMARY:")
        print(f"Total URLs tested: {total_tests}")
        print(f"Successful extractions: {successful_extractions}")
        print(f"Success rate: {(successful_extractions/total_tests)*100:.1f}%")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error setting up driver: {str(e)}")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_final_extractors() 