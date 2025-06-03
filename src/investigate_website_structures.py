"""
Website Structure Investigation Script
This script will examine the HTML structure of failing websites to understand
how to properly extract outstanding shares information
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

def investigate_website_structure(url, site_name):
    """Investigate a single website's structure"""
    print(f"\n{'='*60}")
    print(f"INVESTIGATING: {site_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
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
        
        print(f"Loading page...")
        driver.get(url)
        time.sleep(5)  # Wait for dynamic content
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Get page title
        title = driver.title
        print(f"Page Title: {title}")
        
        # Look for text containing shares-related keywords
        text_content = soup.get_text()
        shares_keywords = [
            'outstanding shares', 'shares outstanding', 'total shares', 'shares issued',
            'issued shares', 'shares in issue', 'number of shares', 'share count',
            'units outstanding', 'outstanding units', 'total units', 'issued units'
        ]
        
        print(f"\nSearching for shares-related text...")
        found_shares_text = []
        
        for keyword in shares_keywords:
            if keyword.lower() in text_content.lower():
                # Find context around the keyword
                pattern = rf'.{{0,100}}{re.escape(keyword)}.{{0,100}}'
                matches = re.finditer(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    context = match.group().strip()
                    if context not in found_shares_text:
                        found_shares_text.append(context)
        
        if found_shares_text:
            print(f"Found {len(found_shares_text)} potential shares references:")
            for i, text in enumerate(found_shares_text[:5], 1):  # Show first 5
                print(f"  {i}. {text}")
        else:
            print("❌ No shares-related text found")
        
        # Look for numbers that could be shares
        print(f"\nSearching for potential share numbers...")
        number_patterns = [
            r'\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:million|mil|m)\b',  # X million
            r'\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:billion|bil|b)\b',  # X billion
            r'\b(\d{1,15}(?:,\d{3})*)\b',  # Large numbers with commas
        ]
        
        potential_numbers = []
        for pattern in number_patterns:
            matches = re.finditer(pattern, text_content, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 50)
                context_end = min(len(text_content), match.end() + 50)
                context = text_content[context_start:context_end].strip()
                potential_numbers.append((match.group(), context))
        
        if potential_numbers:
            print(f"Found {len(potential_numbers)} potential numbers:")
            for i, (number, context) in enumerate(potential_numbers[:10], 1):  # Show first 10
                print(f"  {i}. {number} -> {context}")
        else:
            print("❌ No potential share numbers found")
        
        # Look for common table structures
        print(f"\nAnalyzing table structures...")
        tables = soup.find_all('table')
        if tables:
            print(f"Found {len(tables)} tables")
            for i, table in enumerate(tables[:3], 1):  # Analyze first 3 tables
                print(f"\nTable {i}:")
                rows = table.find_all('tr')
                for j, row in enumerate(rows[:5], 1):  # Show first 5 rows
                    cells = row.find_all(['td', 'th'])
                    row_text = ' | '.join([cell.get_text().strip() for cell in cells])
                    if row_text:
                        print(f"  Row {j}: {row_text}")
        else:
            print("❌ No tables found")
        
        # Look for common div/span structures with classes
        print(f"\nAnalyzing div/span structures...")
        potential_containers = soup.find_all(['div', 'span'], class_=True)
        class_names = set()
        for container in potential_containers:
            if container.get('class'):
                class_names.update(container.get('class'))
        
        relevant_classes = [cls for cls in class_names if any(keyword in cls.lower() for keyword in ['fact', 'data', 'info', 'detail', 'stat', 'fund', 'share', 'unit'])]
        
        if relevant_classes:
            print(f"Found relevant CSS classes: {relevant_classes[:10]}")  # Show first 10
        else:
            print("❌ No relevant CSS classes found")
        
        # Save page source for manual inspection
        filename = f"{site_name.lower().replace(' ', '_')}_page_source.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"\n💾 Page source saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error investigating {site_name}: {str(e)}")
        
    finally:
        if driver:
            driver.quit()

def main():
    """Investigate multiple websites to understand their structures"""
    
    # Set up logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise
    
    # Websites to investigate
    investigation_targets = [
        ("https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd", "Valour"),
        ("https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/", "VanEck"),
        ("https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin", "WisdomTree"),
        ("https://www.proshares.com/our-etfs/strategic/bito", "ProShares"),
        ("https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust", "Grayscale"),
    ]
    
    print("WEBSITE STRUCTURE INVESTIGATION")
    print("=" * 60)
    print("This script will examine the HTML structure of failing websites")
    print("to understand how to properly extract outstanding shares information.")
    print("=" * 60)
    
    for url, site_name in investigation_targets:
        investigate_website_structure(url, site_name)
        time.sleep(2)  # Brief pause between investigations
    
    print(f"\n{'='*60}")
    print("INVESTIGATION COMPLETE")
    print("Check the generated HTML files for manual inspection.")
    print("Look for patterns in the output above to improve extractors.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 