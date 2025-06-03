import re
import logging
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def modify_sixgroup_url(url):
    """
    Modify SIX Group URL to include the product-details section
    """
    # Check if URL already ends with product-details
    if url.endswith('/product-details'):
        return url
    
    # Check if URL already has a hash fragment
    if '#/' in url:
        base_url = url.split('#/')[0]
        return f"{base_url}#/product-details"
    elif url.endswith('#'):
        return f"{url}/product-details"
    elif url.endswith('/'):
        return f"{url}#/product-details"
    else:
        return f"{url}#/product-details"

def extract_sixgroup_shares(driver, url):
    """
    Extract shares outstanding (Number in issue) from SIX Group URLs
    """
    # Modify the URL to point to the product-details section
    modified_url = modify_sixgroup_url(url)
    logging.info(f"Accessing URL: {modified_url}")
    
    try:
        driver.get(modified_url)
        # Wait for the page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Allow extra time for JavaScript content to load
        time.sleep(5)
    except TimeoutException:
        logging.error(f"Timed out waiting for page to load: {modified_url}")
        return {"error": "Timed out waiting for page to load"}

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Specifically look for tables on the product details page
    tables = soup.find_all('table')
    
    for table in tables:
        # For each table, find rows
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
                
            # Check if the first cell contains our target text
            label_cell = cells[0].get_text(strip=True).lower()
            if ('number in issue' in label_cell or 
                'notes outstanding' in label_cell or 
                'shares outstanding' in label_cell):
                
                # Extract the value from the second cell
                value_cell = cells[1].get_text(strip=True)
                logging.info(f"Found target row with label: '{cells[0].get_text(strip=True)}', value: '{value_cell}'")
                
                # Extract number from the value cell
                number_match = re.search(r"([\d\'\,\.]+)", value_cell)
                if number_match:
                    shares_text = number_match.group(1).strip()
                    logging.info(f"Extracted shares value: {shares_text}")
                    
                    # Handle Swiss number format with apostrophes as thousand separators
                    # Example: "535'000" -> "535000"
                    shares_text = shares_text.replace("'", "")
                    
                    # Also handle other thousand separators
                    shares_text = shares_text.replace(",", "").replace(" ", "")
                    
                    try:
                        shares_value = int(shares_text)
                        return {"outstanding_shares": shares_value}
                    except (ValueError, TypeError) as e:
                        logging.error(f"Error parsing shares value '{shares_text}': {e}")
    
    # If we didn't find in tables, look for key-value pairs in divs
    # Look for divs that might contain structured data
    key_value_divs = soup.find_all('div', class_=lambda c: c and ('details' in c.lower() or 'data' in c.lower()))
    
    for container in key_value_divs:
        # Look for labels that might indicate share data
        labels = container.find_all(
            lambda tag: tag.name in ('div', 'span', 'label', 'p') and 
            re.search(r'number\s+in\s+issue|notes?\s+outstanding|shares?\s+outstanding', 
                      tag.get_text(strip=True), 
                      re.IGNORECASE)
        )
        
        for label in labels:
            # Try to find the corresponding value
            # First check the next sibling
            next_element = label.find_next()
            if next_element and re.search(r'[\d\'\,\.]+', next_element.get_text(strip=True)):
                value_text = next_element.get_text(strip=True)
                number_match = re.search(r'([\d\'\,\.]+)', value_text)
                if number_match:
                    shares_text = number_match.group(1).strip()
                    logging.info(f"Found shares in div structure: {shares_text}")
                    
                    # Handle Swiss number format
                    shares_text = shares_text.replace("'", "").replace(",", "").replace(" ", "")
                    
                    try:
                        shares_value = int(shares_text)
                        return {"outstanding_shares": shares_value}
                    except (ValueError, TypeError) as e:
                        logging.error(f"Error parsing div shares value '{shares_text}': {e}")
    
    # Last attempt: Do a complete page scan for specific patterns
    page_text = soup.get_text(" ", strip=True)
    
    # Look for patterns with exact label matches
    patterns = [
        r"Number\s+in\s+issue\s*[:=]?\s*([\d\'\,\.]+)",
        r"Notes?\s+outstanding\s*[:=]?\s*([\d\'\,\.]+)",
        r"Shares?\s+outstanding\s*[:=]?\s*([\d\'\,\.]+)"
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, page_text, re.IGNORECASE)
        for match in matches:
            shares_text = match.group(1).strip()
            logging.info(f"Found shares with regex pattern: {shares_text}")
            
            # Handle Swiss number format
            shares_text = shares_text.replace("'", "").replace(",", "").replace(" ", "")
            
            try:
                shares_value = int(shares_text)
                return {"outstanding_shares": shares_value}
            except (ValueError, TypeError) as e:
                logging.error(f"Error parsing regex shares value '{shares_text}': {e}")
    
    # If we get here, we couldn't find the information
    # Try to diagnose by logging potential candidates
    all_numbers = re.findall(r'[\d\'\,\.]+', page_text)
    logging.info(f"Potential number candidates found: {all_numbers[:10]}")
    
    # Save page source for debugging
    with open("sixgroup_debug_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logging.info(f"Saved page source to sixgroup_debug_page.html for debugging")
    
    logging.error(f"Could not find outstanding shares at: {modified_url}")
    return {"error": "Could not find outstanding shares information"}

def get_sixgroup_shares_outstanding(url):
    """
    Wrapper function to set up WebDriver and extract shares outstanding from SIX Group URL
    """
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        result = extract_sixgroup_shares(driver, url)
        return result
    finally:
        driver.quit()

def test_sixgroup_extractor():
    """
    Test the SIX Group shares outstanding extractor with sample URLs
    """
    test_urls = [
        "https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH1146882316USD4.html#/",
        "https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH0496454155USD4.html#/",
        "https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH0475552201USD4.html#/"
    ]
    
    expected_values = [535000, 14420000, 722703]
    
    print("\nTesting SIX Group shares outstanding extractor...")
    print("-" * 60)
    
    for i, url in enumerate(test_urls):
        print(f"Testing URL: {url}")
        result = get_sixgroup_shares_outstanding(url)
        
        if "error" in result:
            print(f"❌ Failed: {result['error']}")
        else:
            shares = result["outstanding_shares"]
            print(f"Found: {shares:,}")
            
            if shares == expected_values[i]:
                print(f"✅ Success: Value matches expected {expected_values[i]:,}")
            else:
                print(f"❌ Error: Expected {expected_values[i]:,} but got {shares:,}")
                
        print("-" * 60)

if __name__ == "__main__":
    test_sixgroup_extractor() 