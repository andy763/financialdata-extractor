"""
Debug specific websites to understand their structure for outstanding shares extraction
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

def debug_website_content(driver, url, site_name):
    """Debug a specific website's content for outstanding shares"""
    print(f"\n{'='*60}")
    print(f"DEBUGGING: {site_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        # Get page source
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Save page source for manual inspection
        filename = f"{site_name.lower().replace(' ', '_')}_debug.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved page source to: {filename}")
        
        # Search for shares-related text patterns
        shares_patterns = [
            r'outstanding\s+shares?[:\s]*([0-9,.\s]+)',
            r'shares?\s+outstanding[:\s]*([0-9,.\s]+)',
            r'total\s+shares?[:\s]*([0-9,.\s]+)',
            r'shares?\s+issued[:\s]*([0-9,.\s]+)',
            r'number\s+of\s+shares?[:\s]*([0-9,.\s]+)',
            r'([0-9,.\s]+)\s+shares?\s+outstanding',
            r'([0-9,.\s]+)\s+outstanding\s+shares?',
            r'shares?\s+in\s+issue[:\s]*([0-9,.\s]+)',
            r'issued\s+shares?[:\s]*([0-9,.\s]+)',
        ]
        
        text_content = soup.get_text()
        print(f"\nSearching for shares patterns in text content...")
        
        found_patterns = []
        for pattern in shares_patterns:
            matches = re.finditer(pattern, text_content, re.IGNORECASE)
            for match in matches:
                found_patterns.append({
                    'pattern': pattern,
                    'match': match.group(0),
                    'number': match.group(1) if match.groups() else 'N/A'
                })
        
        if found_patterns:
            print(f"Found {len(found_patterns)} potential shares patterns:")
            for i, pattern_info in enumerate(found_patterns[:10], 1):  # Show first 10
                print(f"  {i}. Pattern: {pattern_info['pattern']}")
                print(f"     Match: {pattern_info['match']}")
                print(f"     Number: {pattern_info['number']}")
                print()
        else:
            print("No shares patterns found in text content")
        
        # Look for specific numbers that might be shares
        print(f"\nSearching for large numbers (potential shares)...")
        number_patterns = [
            r'\\b([0-9]{6,12})\\b',  # 6-12 digit numbers
            r'\\b([0-9]{1,3}(?:,[0-9]{3})+)\\b',  # Comma-separated numbers
            r'\\b([0-9]+\\.?[0-9]*\\s*(?:million|billion|thousand))\\b',  # Numbers with units
        ]
        
        large_numbers = []
        for pattern in number_patterns:
            matches = re.finditer(pattern, text_content, re.IGNORECASE)
            for match in matches:
                large_numbers.append(match.group(1))
        
        if large_numbers:
            print(f"Found {len(large_numbers)} large numbers:")
            for i, number in enumerate(set(large_numbers)[:15], 1):  # Show first 15 unique
                print(f"  {i}. {number}")
        else:
            print("No large numbers found")
        
        # Look for table data that might contain shares
        print(f"\nSearching for table data...")
        tables = soup.find_all('table')
        if tables:
            print(f"Found {len(tables)} tables")
            for i, table in enumerate(tables[:3], 1):  # Check first 3 tables
                print(f"  Table {i}:")
                rows = table.find_all('tr')
                for j, row in enumerate(rows[:5], 1):  # Check first 5 rows
                    cells = row.find_all(['td', 'th'])
                    row_text = ' | '.join([cell.get_text().strip() for cell in cells])
                    if any(keyword in row_text.lower() for keyword in ['shares', 'outstanding', 'issued']):
                        print(f"    Row {j}: {row_text}")
        else:
            print("No tables found")
        
        # Look for specific CSS classes or IDs that might contain shares data
        print(f"\nSearching for elements with shares-related classes/IDs...")
        shares_selectors = [
            '[class*="shares"]',
            '[id*="shares"]',
            '[class*="outstanding"]',
            '[id*="outstanding"]',
            '[class*="issued"]',
            '[id*="issued"]',
        ]
        
        for selector in shares_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"  Selector '{selector}' found {len(elements)} elements:")
                for elem in elements[:3]:  # Show first 3
                    print(f"    {elem.name}: {elem.get_text().strip()[:100]}")
        
        print(f"\n{'='*60}")
        
    except Exception as e:
        print(f"Error debugging {site_name}: {e}")

def main():
    """Debug specific websites"""
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Websites to debug
    debug_sites = [
        ("Valour Bitcoin", "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd"),
        ("Grayscale Bitcoin Cash", "https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust"),
        ("ProShares BITO", "https://www.proshares.com/our-etfs/strategic/bito"),
        ("VanEck Bitcoin", "https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/"),
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
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(30)
        
        for site_name, url in debug_sites:
            debug_website_content(driver, url, site_name)
            time.sleep(2)  # Brief pause between sites
        
        print(f"\n{'='*60}")
        print("DEBUGGING COMPLETE")
        print("Check the generated HTML files for manual inspection")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Error setting up driver: {str(e)}")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main() 