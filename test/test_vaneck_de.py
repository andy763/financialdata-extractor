import sys
import os
import logging
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the function we want to test
from src.improved_custom_domain_extractors import extract_vaneck_shares

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_vaneck_de_shares(driver, url):
    """
    Special extractor for VanEck German website (vaneck.com/de/)
    Targeted at finding 'Notes Outstanding' information
    """
    try:
        logging.info(f"Using VanEck DE custom extractor for: {url}")
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Method 1: Look for structured data or key facts sections
        key_facts_sections = soup.find_all(class_=re.compile(r'key-facts|fund-data|fund-info|product-data'))
        for section in key_facts_sections:
            rows = section.find_all('tr') or section.find_all(class_=re.compile(r'row|item'))
            for row in rows:
                text = row.get_text().strip()
                # Look specifically for "Notes Outstanding" pattern
                notes_match = re.search(r'Notes\s+Outstanding[:\s]*([0-9,\.]+)', text, re.IGNORECASE)
                if notes_match:
                    shares = notes_match.group(1).replace(',', '')
                    logging.info(f"Found Notes Outstanding in key facts: {shares}")
                    return shares
        
        # Method 2: Look for tables with Notes Outstanding
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                for i, cell in enumerate(cells):
                    cell_text = cell.get_text().strip()
                    if 'notes' in cell_text.lower() and 'outstanding' in cell_text.lower():
                        # Look for number in next cell
                        if i + 1 < len(cells):
                            next_cell = cells[i + 1]
                            number_match = re.search(r'([0-9,\.]+)', next_cell.get_text().strip())
                            if number_match:
                                shares = number_match.group(1).replace(',', '')
                                logging.info(f"Found Notes Outstanding in table: {shares}")
                                return shares
        
        # Method 3: Look for overview/summary panels 
        summary_sections = soup.find_all(class_=re.compile(r'overview|summary|details|info'))
        for section in summary_sections:
            text = section.get_text()
            notes_match = re.search(r'Notes\s+Outstanding[:\s]*([0-9,\.]+)', text, re.IGNORECASE)
            if notes_match:
                shares = notes_match.group(1).replace(',', '')
                logging.info(f"Found Notes Outstanding in summary: {shares}")
                return shares
        
        # Method 4: Search entire page text for Notes Outstanding pattern
        notes_match = re.search(r'Notes\s+Outstanding[:\s]*([0-9,\.]+)', page_source, re.IGNORECASE)
        if notes_match:
            shares = notes_match.group(1).replace(',', '')
            logging.info(f"Found Notes Outstanding in page text: {shares}")
            return shares
        
        logging.warning("Could not find Notes Outstanding on VanEck DE page")
        return None
        
    except Exception as e:
        logging.error(f"Error in VanEck DE extractor: {str(e)}")
        return None

def run_test():
    """
    Test both the original and new VanEck extractors on the German site
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        # Test URL - VanEck German site with Avalanche ETP
        test_url = "https://www.vaneck.com/de/en/investments/avalanche-etp/overview/"
        
        # Load the page
        driver.get(test_url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5)  # Wait longer for all content to load
        
        # Get the page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Print info about the page
        print("\n----- PAGE ANALYSIS -----")
        
        # Look for "Holdings" tab/section which might contain the Notes Outstanding info
        print("\nChecking if Holdings section is available...")
        holdings_tab = soup.find('a', string=re.compile(r'Holdings', re.IGNORECASE))
        if holdings_tab:
            holdings_href = holdings_tab.get('href')
            print(f"Found Holdings tab with href: {holdings_href}")
            
            # Try to navigate to Holdings tab
            if holdings_href:
                holdings_url = holdings_href if holdings_href.startswith('http') else f"https://www.vaneck.com{holdings_href}"
                print(f"Navigating to Holdings URL: {holdings_url}")
                driver.get(holdings_url)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(5)  # Wait for dynamic content to load
                
                # Get the updated page source
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Look for Notes Outstanding in the Holdings page
                print("\nSearching for 'Notes Outstanding' in Holdings page:")
                notes_text = re.findall(r'(?:Notes\s+Outstanding).{0,50}', page_source, re.IGNORECASE)
                for match in notes_text:
                    print(f"  • {match.strip()}")
        
        # If not found in Holdings, try checking for document links (fact sheets often contain this info)
        print("\nChecking for fact sheet or document links...")
        fact_sheet_links = soup.find_all('a', string=re.compile(r'(?:Fact\s+Sheet|Factsheet)', re.IGNORECASE))
        if fact_sheet_links:
            for link in fact_sheet_links:
                href = link.get('href')
                print(f"Found fact sheet link: {href}")
                
                # For fact sheets we can't easily parse PDFs, so just report we found them
                # In a real implementation, we might want to download and parse these
        
        # Look for any sections that might have "Notes Outstanding" info
        key_terms = ["Notes Outstanding", "Outstanding Notes", "Shares Outstanding", "ETN Outstanding"]
        print("\nSearching for key terms:")
        for term in key_terms:
            print(f"\nLooking for '{term}':")
            term_regex = re.compile(f"{term}.{{0,50}}", re.IGNORECASE)
            matches = re.findall(term_regex, page_source)
            if matches:
                for match in matches:
                    print(f"  • {match.strip()}")
            else:
                print("  (No matches found)")
                
        # Look for any data that might represent outstanding shares/notes
        print("\nPotential data values (looking for numbers around 5,853,000):")
        number_regex = re.compile(r'(\d{1,3}(?:,\d{3}){1,2})')  # Looking for numbers like 1,234,567
        number_matches = re.findall(number_regex, page_source)
        for match in number_matches:
            # Clean number and check if it's close to our expected value
            clean_num = int(match.replace(',', ''))
            if 5800000 <= clean_num <= 5900000:  # Range around 5,853,000
                context = re.search(f".{{0,30}}{match}.{{0,30}}", page_source)
                if context:
                    print(f"  • {context.group(0).strip()}")
        
        # If we haven't found it yet, try getting info from the Portfolio tab
        print("\nChecking Portfolio tab for shares information...")
        portfolio_tab = soup.find('a', string=re.compile(r'Portfolio', re.IGNORECASE))
        if portfolio_tab:
            portfolio_href = portfolio_tab.get('href')
            if portfolio_href:
                portfolio_url = portfolio_href if portfolio_href.startswith('http') else f"https://www.vaneck.com{portfolio_href}"
                print(f"Navigating to Portfolio URL: {portfolio_url}")
                driver.get(portfolio_url)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(5)  # Wait for dynamic content to load
                
                # Get the updated page source
                page_source = driver.page_source
                
                # Look for Notes Outstanding in the Portfolio page
                print("\nSearching for 'Notes Outstanding' in Portfolio page:")
                notes_text = re.findall(r'(?:Notes\s+Outstanding).{0,50}', page_source, re.IGNORECASE)
                for match in notes_text:
                    print(f"  • {match.strip()}")
                    
                # Look for numbers similar to our expected value
                print("\nPotential matches in Portfolio page:")
                soup = BeautifulSoup(page_source, 'html.parser')
                number_matches = re.findall(number_regex, page_source)
                for match in number_matches:
                    # Clean number and check if it's close to our expected value
                    clean_num = int(match.replace(',', ''))
                    if 5800000 <= clean_num <= 5900000:  # Range around 5,853,000
                        context = re.search(f".{{0,30}}{match}.{{0,30}}", page_source)
                        if context:
                            print(f"  • {context.group(0).strip()}")
                            
        # Now run the tests with our original extractors
        # Test the original extractor
        logging.info(f"Testing original VanEck extractor on: {test_url}")
        result_original = extract_vaneck_shares(driver, test_url)
        logging.info(f"Original extractor result: {result_original}")
        
        # Test the new German-specific extractor
        logging.info(f"Testing new VanEck DE extractor on: {test_url}")
        result_new = extract_vaneck_de_shares(driver, test_url)
        logging.info(f"New DE extractor result: {result_new}")
        
        # Print the comparison results
        print("\n----- TEST RESULTS -----")
        print(f"URL: {test_url}")
        print(f"Original VanEck extractor: {result_original or 'No result'}")
        print(f"New VanEck DE extractor: {result_new or 'No result'}")
        print("Expected value: 5,853,000")
        print("-----------------------\n")
        
        if result_original == "5853000":
            print("✅ Original extractor works correctly!")
        else:
            print("❌ Original extractor failed or returned incorrect value")
            
        if result_new == "5853000":
            print("✅ New DE extractor works correctly!")
        else:
            print("❌ New DE extractor failed or returned incorrect value")
        
    except Exception as e:
        logging.error(f"Test error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_test() 