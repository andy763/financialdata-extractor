import requests
import re
import logging
import sys
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def extract_shares_from_globalx(url):
    """
    Direct HTTP approach to extract shares outstanding from GlobalX ETFs website
    
    IMPORTANT: As per requirements, this extractor NEVER uses hardcoded values.
    If extraction fails, it will return None (error).
    """
    logging.info(f"Attempting to extract shares from: {url}")
    
    # Check if URL has #trading anchor; if not, add it
    if "#trading" not in url:
        url = url + "#trading"
    
    try:
        # Fetch the page content
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch URL: {url}, status code: {response.status_code}")
            return None
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strategy 1: Look for table with shares outstanding information
        logging.info("Searching for shares outstanding in tables")
        tables = soup.find_all('table')
        
        for table in tables:
            table_text = table.get_text().lower()
            if 'shares outstanding' in table_text or 'outstanding shares' in table_text:
                logging.info("Found table with shares outstanding information")
                
                # Check each row for shares outstanding
                rows = table.find_all('tr')
                for row in rows:
                    row_text = row.get_text().lower()
                    if 'shares outstanding' in row_text or 'outstanding shares' in row_text:
                        # Extract cells from this row
                        cells = row.find_all('td')
                        
                        # Skip if row doesn't have enough cells
                        if len(cells) < 2:
                            continue
                        
                        # Try to find a cell with numeric value
                        for cell in cells:
                            cell_text = cell.get_text().strip()
                            # Look for number patterns
                            shares_match = re.search(r'([\d,\.]+)', cell_text)
                            if shares_match:
                                shares_str = shares_match.group(1)
                                logging.info(f"Found shares outstanding in table: {shares_str}")
                                return shares_str
        
        # Strategy 2: Look for specific patterns in any element
        logging.info("Searching for shares outstanding in any element")
        elements = soup.find_all(['div', 'p', 'span', 'li'])
        
        for element in elements:
            element_text = element.get_text().lower()
            if 'shares outstanding' in element_text or 'outstanding shares' in element_text:
                # Try to extract number
                shares_match = re.search(r'shares\s+outstanding:?\s*([\d,\.]+)', element_text, re.IGNORECASE)
                if not shares_match:
                    shares_match = re.search(r'outstanding\s+shares:?\s*([\d,\.]+)', element_text, re.IGNORECASE)
                
                if shares_match:
                    shares_str = shares_match.group(1)
                    logging.info(f"Found shares outstanding in element: {shares_str}")
                    return shares_str
        
        # Strategy 3: Look for the pattern anywhere in the page text
        logging.info("Searching for shares outstanding in entire page")
        page_text = soup.get_text()
        
        shares_match = re.search(r'shares\s+outstanding:?\s*([\d,\.]+)', page_text, re.IGNORECASE)
        if not shares_match:
            shares_match = re.search(r'outstanding\s+shares:?\s*([\d,\.]+)', page_text, re.IGNORECASE)
        
        if shares_match:
            shares_str = shares_match.group(1)
            logging.info(f"Found shares outstanding in page text: {shares_str}")
            return shares_str
        
        # If we get here, we couldn't find the shares outstanding
        # NO HARDCODED VALUES USED - THROW AN ERROR INSTEAD
        logging.error("Could not find shares outstanding on the page - NO HARDCODED FALLBACKS USED")
        return None
        
    except Exception as e:
        logging.error(f"Error extracting from {url}: {str(e)}")
        return None

def main():
    """
    Test the direct scraper with known URLs
    """
    test_urls = [
        "https://globalxetfs.eu/funds/et0x/#trading",  # Example from the requirements
        "https://globalxetfs.eu/funds/bt0x/#holdings"   # Additional example to test
    ]
    
    for url in test_urls:
        shares = extract_shares_from_globalx(url)
        if shares:
            logging.info(f"Successfully extracted shares for {url}: {shares}")
        else:
            logging.error(f"Failed to extract shares for {url}")

if __name__ == "__main__":
    main() 