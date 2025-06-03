#!/usr/bin/env python3
"""
Comprehensive Fix Script for Colored Cell Issues (Rows 2-178)

This script addresses specific issues identified in the Excel file:
- Purple cells: Wrong figures extracted
- Red cells: Hard errors in cells  
- Orange cells: .0 rounding errors
- Light Green: AI got right (no action needed)
- Dark Green: AI got wrong (needs improvement)

Based on the analysis of the codebase and error patterns.
"""

import re
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def enhanced_grayscale_price_extraction(driver, url):
    """
    Enhanced Grayscale price extraction with multiple fallback methods.
    Addresses issues with rows that had wrong figures or AI failures.
    """
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)  # Extended wait for JavaScript content
    except TimeoutException:
        raise ValueError("Timed out waiting for Grayscale page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for market price in structured data
    try:
        # Look for JSON-LD structured data
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict) and 'price' in data:
                    price_str = str(data['price']).replace('$', '').replace(',', '')
                    price = float(price_str)
                    if 0.01 <= price <= 10000:
                        logging.info(f"Grayscale: Found price in structured data: ${price}")
                        return price
            except:
                continue
    except Exception as e:
        logging.debug(f"Grayscale structured data method failed: {e}")

    # Method 2: Enhanced regex patterns for price extraction
    page_text = soup.get_text(" ", strip=True)
    
    # More specific patterns for Grayscale pages
    price_patterns = [
        r'Market\s+Price[:\s]*\$?\s*([\d,]+\.?\d*)',
        r'Share\s+Price[:\s]*\$?\s*([\d,]+\.?\d*)',
        r'Current\s+Price[:\s]*\$?\s*([\d,]+\.?\d*)',
        r'NAV[:\s]*\$?\s*([\d,]+\.?\d*)',
        r'Last\s+Price[:\s]*\$?\s*([\d,]+\.?\d*)',
        r'Price[:\s]*\$?\s*([\d,]+\.?\d*)',
        r'\$\s*([\d,]+\.?\d*)\s*(?:per\s+share|USD)',
    ]
    
    for pattern in price_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        for match in matches:
            try:
                price_str = match.replace(',', '')
                price = float(price_str)
                # Validate price range for Grayscale ETFs
                if 1.0 <= price <= 500.0:
                    logging.info(f"Grayscale: Found price with pattern '{pattern}': ${price}")
                    return price
            except ValueError:
                continue
    
    # Method 3: Look for price in table cells or specific containers
    try:
        # Look for price in table cells
        tables = soup.find_all('table')
        for table in tables:
            cells = table.find_all(['td', 'th'])
            for i, cell in enumerate(cells):
                cell_text = cell.get_text(strip=True)
                if any(keyword in cell_text.lower() for keyword in ['price', 'nav', 'market']):
                    # Check next few cells for price value
                    for j in range(i+1, min(i+4, len(cells))):
                        next_cell = cells[j].get_text(strip=True)
                        price_match = re.search(r'\$?\s*([\d,]+\.?\d*)', next_cell)
                        if price_match:
                            try:
                                price = float(price_match.group(1).replace(',', ''))
                                if 1.0 <= price <= 500.0:
                                    logging.info(f"Grayscale: Found price in table: ${price}")
                                    return price
                            except ValueError:
                                continue
    except Exception as e:
        logging.debug(f"Grayscale table method failed: {e}")
    
    raise ValueError("Could not extract valid price from Grayscale page")

def enhanced_morningstar_price_extraction(driver, url):
    """
    Enhanced Morningstar price extraction for Belgian/European sites.
    Addresses purple cell issues with wrong figures.
    """
    # Check if it's a PDF URL first
    if 'format=pdf' in url.lower() or url.lower().endswith('.pdf'):
        raise ValueError("PDF URL cannot be processed for price extraction")
    
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(10)  # Extended wait for Morningstar's heavy JavaScript
    except TimeoutException:
        raise ValueError("Timed out waiting for Morningstar page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for NAV or price in specific Morningstar containers
    try:
        # Look for price containers with common Morningstar classes
        price_containers = soup.find_all(['div', 'span', 'td'], 
                                       class_=re.compile(r'(price|nav|value|quote)', re.I))
        for container in price_containers:
            text = container.get_text(strip=True)
            # Look for European number format (123,45 EUR or 123.45 USD)
            price_match = re.search(r'([\d,]+\.?\d*)\s*(?:EUR|USD|€|\$)', text)
            if price_match:
                try:
                    price_str = price_match.group(1)
                    # Handle European format (123,45 -> 123.45)
                    if ',' in price_str and '.' not in price_str:
                        price_str = price_str.replace(',', '.')
                    elif ',' in price_str and '.' in price_str:
                        # Format like 1.234,56 -> 1234.56
                        price_str = price_str.replace('.', '').replace(',', '.')
                    
                    price = float(price_str)
                    if 0.1 <= price <= 10000:
                        logging.info(f"Morningstar: Found price in container: {price}")
                        return price
                except ValueError:
                    continue
    except Exception as e:
        logging.debug(f"Morningstar container method failed: {e}")
    
    # Method 2: Look for price in data attributes
    try:
        elements_with_data = soup.find_all(attrs={'data-value': True})
        for element in elements_with_data:
            data_value = element.get('data-value', '')
            try:
                price = float(data_value)
                if 0.1 <= price <= 10000:
                    logging.info(f"Morningstar: Found price in data attribute: {price}")
                    return price
            except ValueError:
                continue
    except Exception as e:
        logging.debug(f"Morningstar data attribute method failed: {e}")
    
    # Method 3: Enhanced text pattern matching
    page_text = soup.get_text(" ", strip=True)
    
    # Patterns for European Morningstar sites
    patterns = [
        r'NAV[:\s]*([\d,]+\.?\d*)\s*(?:EUR|USD|€|\$)',
        r'Price[:\s]*([\d,]+\.?\d*)\s*(?:EUR|USD|€|\$)',
        r'Value[:\s]*([\d,]+\.?\d*)\s*(?:EUR|USD|€|\$)',
        r'Quote[:\s]*([\d,]+\.?\d*)\s*(?:EUR|USD|€|\$)',
        r'([\d,]+\.?\d*)\s*(?:EUR|USD|€|\$)\s*(?:per\s+share|per\s+unit)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        for match in matches:
            try:
                price_str = match
                # Handle European number format
                if ',' in price_str and '.' not in price_str:
                    price_str = price_str.replace(',', '.')
                elif ',' in price_str and '.' in price_str:
                    price_str = price_str.replace('.', '').replace(',', '.')
                
                price = float(price_str)
                if 0.1 <= price <= 10000:
                    logging.info(f"Morningstar: Found price with pattern: {price}")
                    return price
            except ValueError:
                continue
    
    raise ValueError("Could not extract valid price from Morningstar page")

def enhanced_valour_price_extraction(driver, url):
    """
    Enhanced Valour price extraction to fix .0 errors.
    Addresses orange cell issues with incorrect decimal values.
    """
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(8)  # Wait for dynamic content
    except TimeoutException:
        raise ValueError("Timed out waiting for Valour page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for real-time price data
    try:
        # Look for price in JavaScript variables or data attributes
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for price variables in JavaScript
                price_matches = re.findall(r'(?:price|value|quote)["\']?\s*:\s*["\']?([\d.]+)', 
                                         script.string, re.IGNORECASE)
                for match in price_matches:
                    try:
                        price = float(match)
                        # Valour products typically have decimal prices
                        if 0.01 <= price <= 1000 and '.' in match:
                            logging.info(f"Valour: Found price in JavaScript: {price}")
                            return price
                    except ValueError:
                        continue
    except Exception as e:
        logging.debug(f"Valour JavaScript method failed: {e}")
    
    # Method 2: Look for price in specific containers
    try:
        # Look for price containers
        price_elements = soup.find_all(['div', 'span', 'p'], 
                                     class_=re.compile(r'(price|value|quote|nav)', re.I))
        for element in price_elements:
            text = element.get_text(strip=True)
            # Look for decimal prices (avoid .0 values)
            price_match = re.search(r'([\d]+\.[\d]{2,})', text)
            if price_match:
                try:
                    price = float(price_match.group(1))
                    if 0.01 <= price <= 1000:
                        logging.info(f"Valour: Found decimal price: {price}")
                        return price
                except ValueError:
                    continue
    except Exception as e:
        logging.debug(f"Valour container method failed: {e}")
    
    # Method 3: Enhanced pattern matching avoiding .0 values
    page_text = soup.get_text(" ", strip=True)
    
    patterns = [
        r'Current\s+Price[:\s]*([\d]+\.[\d]{2,})',  # Require at least 2 decimal places
        r'Market\s+Price[:\s]*([\d]+\.[\d]{2,})',
        r'NAV[:\s]*([\d]+\.[\d]{2,})',
        r'Value[:\s]*([\d]+\.[\d]{2,})',
        r'Price[:\s]*([\d]+\.[\d]{2,})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        for match in matches:
            try:
                price = float(match)
                if 0.01 <= price <= 1000:
                    logging.info(f"Valour: Found price with pattern: {price}")
                    return price
            except ValueError:
                continue
    
    raise ValueError("Could not extract valid decimal price from Valour page")

def enhanced_bitcap_price_extraction(driver, url):
    """
    Enhanced Bitcap price extraction with cookie consent handling.
    Addresses red cell errors due to consent barriers.
    """
    driver.get(url)
    
    # Handle cookie consent
    try:
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Look for and click cookie consent buttons
        consent_selectors = [
            "button[id*='accept']",
            "button[class*='accept']",
            "button[id*='consent']",
            "button[class*='consent']",
            "a[id*='accept']",
            "a[class*='accept']",
            ".cookie-accept",
            "#cookie-accept",
            ".accept-cookies",
            "#accept-cookies"
        ]
        
        for selector in consent_selectors:
            try:
                consent_button = driver.find_element(By.CSS_SELECTOR, selector)
                if consent_button.is_displayed():
                    consent_button.click()
                    logging.info(f"Bitcap: Clicked consent button with selector: {selector}")
                    time.sleep(3)
                    break
            except:
                continue
        
        # Additional wait for content to load after consent
        time.sleep(8)
        
    except TimeoutException:
        raise ValueError("Timed out waiting for Bitcap page to load")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Check if we're still blocked by consent
    page_text = soup.get_text(" ", strip=True).lower()
    if any(keyword in page_text for keyword in ['cookie', 'consent', 'accept', 'privacy']):
        if len(page_text) < 1000:  # Likely a consent page
            raise ValueError("Blocked by cookie consent - manual intervention needed")
    
    # Method 1: Look for fund price information
    try:
        # Look for price in fund information sections
        fund_sections = soup.find_all(['div', 'section'], 
                                    class_=re.compile(r'(fund|price|nav|performance)', re.I))
        for section in fund_sections:
            text = section.get_text(strip=True)
            price_match = re.search(r'([\d,]+\.[\d]{2,})\s*(?:EUR|USD|€|\$)', text)
            if price_match:
                try:
                    price_str = price_match.group(1).replace(',', '')
                    price = float(price_str)
                    if 0.1 <= price <= 10000:
                        logging.info(f"Bitcap: Found price in fund section: {price}")
                        return price
                except ValueError:
                    continue
    except Exception as e:
        logging.debug(f"Bitcap fund section method failed: {e}")
    
    # Method 2: Look for price in tables
    try:
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                for i, cell in enumerate(cells):
                    cell_text = cell.get_text(strip=True).lower()
                    if any(keyword in cell_text for keyword in ['price', 'nav', 'value', 'quote']):
                        # Look for price in adjacent cells
                        for j in range(max(0, i-1), min(len(cells), i+3)):
                            if j != i:
                                price_text = cells[j].get_text(strip=True)
                                price_match = re.search(r'([\d,]+\.[\d]{2,})', price_text)
                                if price_match:
                                    try:
                                        price = float(price_match.group(1).replace(',', ''))
                                        if 0.1 <= price <= 10000:
                                            logging.info(f"Bitcap: Found price in table: {price}")
                                            return price
                                    except ValueError:
                                        continue
    except Exception as e:
        logging.debug(f"Bitcap table method failed: {e}")
    
    raise ValueError("Could not extract valid price from Bitcap page")

def enhanced_invesco_price_extraction(driver, url):
    """
    Enhanced Invesco price extraction with cookie consent handling.
    Addresses red cell errors due to consent barriers.
    """
    driver.get(url)
    
    # Handle cookie consent for Invesco
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Invesco-specific consent handling
        consent_selectors = [
            "#onetrust-accept-btn-handler",
            ".onetrust-accept-btn-handler",
            "button[id*='accept-all']",
            "button[class*='accept-all']",
            "#cookie-accept",
            ".cookie-accept",
            "button[aria-label*='Accept']",
            "button[title*='Accept']"
        ]
        
        for selector in consent_selectors:
            try:
                consent_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                consent_button.click()
                logging.info(f"Invesco: Clicked consent button with selector: {selector}")
                time.sleep(5)
                break
            except:
                continue
        
        # Additional wait for content
        time.sleep(10)
        
    except TimeoutException:
        logging.warning("Invesco: Timeout waiting for page, proceeding anyway")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Method 1: Look for ETF price data
    try:
        # Look for price in ETF-specific containers
        etf_containers = soup.find_all(['div', 'section'], 
                                     class_=re.compile(r'(etf|fund|price|nav|quote)', re.I))
        for container in etf_containers:
            text = container.get_text(strip=True)
            # Look for price patterns
            price_patterns = [
                r'NAV[:\s]*([\d,]+\.[\d]{2,})',
                r'Price[:\s]*([\d,]+\.[\d]{2,})',
                r'Market\s+Price[:\s]*([\d,]+\.[\d]{2,})',
                r'Current\s+Price[:\s]*([\d,]+\.[\d]{2,})',
                r'([\d,]+\.[\d]{2,})\s*(?:GBP|USD|EUR|£|\$|€)'
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        price = float(match.replace(',', ''))
                        if 0.1 <= price <= 10000:
                            logging.info(f"Invesco: Found price with pattern: {price}")
                            return price
                    except ValueError:
                        continue
    except Exception as e:
        logging.debug(f"Invesco container method failed: {e}")
    
    # Method 2: Look for price in data tables
    try:
        tables = soup.find_all('table')
        for table in tables:
            # Look for fund data tables
            table_text = table.get_text(" ", strip=True)
            if any(keyword in table_text.lower() for keyword in ['nav', 'price', 'fund', 'etf']):
                cells = table.find_all(['td', 'th'])
                for cell in cells:
                    cell_text = cell.get_text(strip=True)
                    price_match = re.search(r'([\d,]+\.[\d]{2,})', cell_text)
                    if price_match:
                        try:
                            price = float(price_match.group(1).replace(',', ''))
                            if 0.1 <= price <= 10000:
                                logging.info(f"Invesco: Found price in table: {price}")
                                return price
                        except ValueError:
                            continue
    except Exception as e:
        logging.debug(f"Invesco table method failed: {e}")
    
    raise ValueError("Could not extract valid price from Invesco page")

def test_enhanced_functions():
    """
    Test the enhanced extraction functions with sample URLs.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # Test cases for different issue types
        test_cases = [
            {
                'function': enhanced_grayscale_price_extraction,
                'url': 'https://www.grayscale.com/funds/grayscale-chainlink-trust',
                'description': 'Grayscale (Purple cell fix)'
            },
            {
                'function': enhanced_valour_price_extraction,
                'url': 'https://valour.com/en/products/valour-cardano',
                'description': 'Valour (Orange cell .0 fix)'
            }
        ]
        
        for test_case in test_cases:
            try:
                logging.info(f"Testing {test_case['description']}")
                price = test_case['function'](driver, test_case['url'])
                logging.info(f"✅ SUCCESS: {test_case['description']} - Price: {price}")
            except Exception as e:
                logging.error(f"❌ FAILED: {test_case['description']} - Error: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Enhanced Price Extraction Functions for Colored Cell Issues")
    print("=" * 60)
    print("This script provides enhanced extraction functions for:")
    print("- Purple cells: Wrong figures (Grayscale, Morningstar)")
    print("- Red cells: Hard errors (Bitcap, Invesco consent issues)")
    print("- Orange cells: .0 errors (Valour decimal precision)")
    print("- Dark Green: AI improvements needed")
    print()
    
    # Run tests
    test_enhanced_functions() 