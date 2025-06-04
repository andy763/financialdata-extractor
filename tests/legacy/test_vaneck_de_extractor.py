"""
Test script for VanEck DE extractor with "Notes Outstanding" label support
This script tests the updated custom domain extractor for VanEck DE URLs.
"""

import sys
import logging
import time
import re
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a console handler for direct output
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def print_exception():
    """Print the exception details"""
    print("\n" + "="*80)
    print("EXCEPTION OCCURRED:")
    traceback.print_exc()
    print("="*80 + "\n")

try:
    # Import the custom extractor
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    from custom_domain_extractors import extract_vaneck_de_shares
    print("Successfully imported custom_domain_extractors")
except Exception as e:
    print_exception()
    print(f"Failed to import custom_domain_extractors: {e}")
    sys.exit(1)

def setup_driver():
    """Set up Selenium WebDriver with appropriate options"""
    try:
        print("Setting up Chrome WebDriver...")
        chrome_options = Options()
        
        # Comment out the line below to run in visible mode (recommended for debugging)
        # chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Add user agent to avoid detection
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        print("Chrome WebDriver setup completed successfully")
        return driver
    except Exception as e:
        print_exception()
        print(f"Failed to set up WebDriver: {e}")
        sys.exit(1)

def search_pdf_for_shares(pdf_content):
    """
    Search for shares outstanding information in PDF content
    Returns the shares value if found, None otherwise
    """
    try:
        print(f"Searching PDF content (size: {len(pdf_content)} bytes)")
        
        # Try multiple patterns for the "Notes Outstanding" label
        patterns = [
            rb'Notes\s+Outstanding\s*[:\-–—]?\s*(\d{1,3}(?:[,\.\s]\d{3})+|\d{4,})',
            rb'Notes\s+Outstanding\s*[:\-–—]?\s*([0-9][,\.\s][0-9]+)',
            rb'Notes\s+Outstanding.*?(\d{1,3}(?:[,\.\s]\d{3})+|\d{4,})',
            rb'Outstanding\s+Notes\s*[:\-–—]?\s*(\d{1,3}(?:[,\.\s]\d{3})+|\d{4,})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, pdf_content)
            if match:
                result = match.group(1).decode('utf-8', errors='ignore')
                print(f"Pattern match found: {result}")
                return result
        
        # If specific patterns don't match, try a more general approach
        # Look for the term first, then find nearby numbers
        notes_pos = pdf_content.find(b'Notes Outstanding')
        if notes_pos != -1:
            print(f"Found 'Notes Outstanding' at position {notes_pos}")
            # Look at a chunk of text after the term
            chunk = pdf_content[notes_pos:notes_pos+200]
            print(f"Chunk around 'Notes Outstanding': {chunk}")
            # Find all numbers in this chunk
            numbers = re.findall(rb'(\d{1,3}(?:[,\.\s]\d{3})+|\d{4,})', chunk)
            if numbers:
                result = numbers[0].decode('utf-8', errors='ignore')
                print(f"Found number near 'Notes Outstanding': {result}")
                return result
        else:
            print("Term 'Notes Outstanding' not found in PDF")
        
        return None
    except Exception as e:
        print_exception()
        print(f"Error in search_pdf_for_shares: {e}")
        return None

def test_direct_pdf_extraction():
    """Test direct PDF extraction as a fallback method"""
    print("\n" + "="*80)
    print("TESTING DIRECT PDF EXTRACTION")
    print("="*80)
    
    # Sample PDF URLs for testing
    pdf_urls = [
        "https://www.vaneck.com/de/en/library/fact-sheets/vava-fact-sheet.pdf",  # Avalanche
        "https://www.vaneck.com/de/en/library/fact-sheets/vbtc-fact-sheet.pdf",  # Bitcoin
        "https://www.vaneck.com/de/en/library/fact-sheets/vpol-fact-sheet.pdf",  # Polygon
        "https://www.vaneck.com/de/en/library/fact-sheets/vlnk-fact-sheet.pdf"   # Chainlink
    ]
    
    success_count = 0
    results = {}
    
    for pdf_url in pdf_urls:
        try:
            product_name = pdf_url.split('/')[-1].split('-fact-sheet')[0]
            print(f"\nDownloading PDF for {product_name}: {pdf_url}")
            
            response = requests.get(pdf_url, timeout=20)
            
            if response.status_code == 200:
                pdf_content = response.content
                print(f"PDF download successful - size: {len(pdf_content)} bytes")
                
                # Check if PDF contains 'Notes Outstanding'
                has_term = b'Notes Outstanding' in pdf_content
                print(f"PDF contains 'Notes Outstanding': {has_term}")
                
                # Look for "Notes Outstanding" in the content
                shares_str = search_pdf_for_shares(pdf_content)
                
                if shares_str:
                    # Clean up the shares string
                    cleaned = shares_str.replace('.', '').replace(',', '').replace(' ', '').replace('\u202F', '')
                    try:
                        value = int(cleaned)
                        if 10000 <= value <= 1000000000:
                            formatted_shares = f"{value:,}"
                            print(f"SUCCESS: Found shares in {product_name} PDF: {formatted_shares}")
                            results[product_name] = formatted_shares
                            success_count += 1
                        else:
                            print(f"WARNING: Found value {value} is outside expected range for {product_name}")
                    except ValueError:
                        print(f"WARNING: Could not parse value '{shares_str}' for {product_name}")
                else:
                    # Try to find any occurrences of 'Notes' or 'Outstanding'
                    notes_pos = pdf_content.find(b'Notes')
                    out_pos = pdf_content.find(b'Outstanding')
                    
                    if notes_pos != -1:
                        context = pdf_content[max(0, notes_pos-20):notes_pos+100]
                        print(f"Found 'Notes' at position {notes_pos} with context: {context}")
                    
                    if out_pos != -1:
                        context = pdf_content[max(0, out_pos-20):out_pos+100]
                        print(f"Found 'Outstanding' at position {out_pos} with context: {context}")
                    
                    print(f"FAILED: Could not find 'Notes Outstanding' in {product_name} PDF")
            else:
                print(f"FAILED: Could not download PDF, status code: {response.status_code}")
        
        except Exception as e:
            print_exception()
            print(f"Error processing PDF {pdf_url}: {e}")
    
    print(f"\nPDF extraction test complete. Success: {success_count}/{len(pdf_urls)}")
    
    # Print summary of results
    if success_count > 0:
        print("\n=== PDF EXTRACTION RESULTS ===")
        for product, shares in results.items():
            print(f"{product}: {shares}")
    
    return success_count, results

def manual_test_examples():
    """
    Test the extraction using known examples with hardcoded values for testing purposes.
    This function is just for testing/verification and doesn't use hardcoded values in production.
    """
    print("\n" + "="*80)
    print("MANUAL TEST EXAMPLES")
    print("="*80)
    
    # Test data showing "Notes Outstanding" label with values
    test_data = [
        {"name": "Avalanche", "value": "5,853,000"},
        {"name": "Bitcoin", "value": "13,113,000"},
        {"name": "Polygon", "value": "1,561,000"},
        {"name": "Chainlink", "value": "800,000"}
    ]
    
    for item in test_data:
        print(f"Example: {item['name']} should have Notes Outstanding: {item['value']}")
    
    print("These values should be found by the PDF extraction or the page extractor")
    return True

def test_vaneck_de_extractor(pdf_results=None):
    """
    Test the VanEck DE extractor with multiple URLs to verify it can extract
    outstanding shares information with the "Notes Outstanding" label.
    """
    print("\n" + "="*80)
    print("TESTING VANECK DE EXTRACTOR")
    print("="*80)
    
    driver = None
    
    try:
        driver = setup_driver()
        
        # Test URLs - a mix of various VanEck DE products with correct structure
        test_urls = [
            "https://www.vaneck.com/de/en/investments/avalanche-etp/overview/",
            "https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/",
            "https://www.vaneck.com/de/en/investments/polygon-etp/overview/",
            "https://www.vaneck.com/de/en/investments/chainlink-etp/overview/"
        ]
        
        results = {}
        
        # First try manually adding a comparison
        if pdf_results:
            print("Using PDF results for comparison:")
            for product, shares in pdf_results.items():
                print(f"  {product}: {shares}")
        
        for url in test_urls:
            product = url.split("/")[-3]  # Get product name from URL
            print(f"\nTesting URL: {url}")
            
            try:
                result = extract_vaneck_de_shares(driver, url)
                results[url] = result
                
                # Print the result
                if "outstanding_shares" in result:
                    print(f"SUCCESS: Found outstanding shares for {product}: {result['outstanding_shares']}")
                    
                    # Compare with PDF results if available
                    if pdf_results and product in pdf_results:
                        pdf_value = pdf_results[product]
                        page_value = result['outstanding_shares']
                        if pdf_value == page_value:
                            print(f"MATCH: PDF and page values match for {product}")
                        else:
                            print(f"MISMATCH: PDF value ({pdf_value}) differs from page value ({page_value}) for {product}")
                else:
                    print(f"FAILED: Could not find outstanding shares for {product}. Error: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print_exception()
                print(f"Error testing URL {url}: {e}")
            
            # Add a delay between requests
            time.sleep(2)
        
        # Summary of results
        print("\n" + "="*80)
        print("TEST RESULTS SUMMARY")
        print("="*80)
        
        success_count = sum(1 for r in results.values() if "outstanding_shares" in r)
        print(f"Total URLs tested: {len(test_urls)}")
        print(f"Successful extractions: {success_count}")
        print(f"Failed extractions: {len(test_urls) - success_count}")
        
        for url, result in results.items():
            product = url.split("/")[-3]  # Get product name from URL
            if "outstanding_shares" in result:
                print(f"{product}: {result['outstanding_shares']}")
            else:
                print(f"{product}: FAILED - {result.get('error', 'Unknown error')}")
                
    except Exception as e:
        print_exception()
        print(f"Error during testing: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    try:
        print("Starting VanEck DE extractor test...")
        
        # Show manual test examples
        manual_test_examples()
        
        # First test the direct PDF extraction as a fallback
        pdf_success, pdf_results = test_direct_pdf_extraction()
        
        # Then test the full extractor
        if pdf_success > 0:
            print("PDF extraction works! Now testing the full extractor...")
            test_vaneck_de_extractor(pdf_results)
        else:
            print("PDF extraction didn't find values. Testing the web extractor anyway...")
            test_vaneck_de_extractor()
    except Exception as e:
        print_exception()
        print(f"Test script error: {e}")
        sys.exit(1) 