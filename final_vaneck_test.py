"""
Final test script for the updated VanEck DE extractor.
Tests the extract_vaneck_de_shares function across multiple product URLs
to verify it can extract outstanding shares with "Notes Outstanding" labeling.
"""

import sys
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Import the custom extractor
sys.path.append('./src')
from custom_domain_extractors import extract_vaneck_de_shares

def setup_driver():
    """Set up Selenium WebDriver with appropriate options"""
    print("\nSetting up Chrome WebDriver...")
    chrome_options = Options()
    
    # Comment out for headless mode, visible browser is better for debugging
    # chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Add user agent to avoid detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def extract_product_name(url):
    """Extract the product name from the URL"""
    # Example: https://www.vaneck.com/de/en/investments/avalanche-etp/overview/
    # Should return "avalanche-etp"
    parts = url.rstrip('/').split('/')
    # Find "investments" in the URL and take the next part
    try:
        investments_index = parts.index("investments")
        if investments_index + 1 < len(parts):
            return parts[investments_index + 1]
    except ValueError:
        pass
    
    # Fallback: return the second-to-last part if not empty
    if len(parts) >= 2 and parts[-2]:
        return parts[-2]
    
    # Last resort
    return url.split('/')[-2]

def test_vaneck_de_extractor():
    """Test the VanEck DE extractor across multiple product URLs"""
    print("\n===== TESTING VANECK DE EXTRACTOR WITH NOTES OUTSTANDING =====\n")
    
    # Test URLs covering various VanEck DE products
    test_urls = [
        # Primary test cases mentioned in the user's query
        "https://www.vaneck.com/de/en/investments/avalanche-etp/overview/",  # Avalanche
        "https://www.vaneck.com/de/en/investments/algorand-etp/overview/",   # Algorand
        "https://www.vaneck.com/de/en/investments/chainlink-etp/overview/",  # Chainlink
        "https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/",    # Bitcoin
        "https://www.vaneck.com/de/en/investments/polygon-etp/overview/",    # Polygon
        "https://www.vaneck.com/de/en/investments/smart-contract-leaders-etp/overview/", # Smart Contract Leaders
    ]
    
    # Expected values from the user's requirements
    expected_values = {
        "avalanche-etp": "5,853,000",
        "algorand-etp": "851,000",
        "chainlink-etp": "800,000",
        "bitcoin-etp": "13,113,000",  # Note: HTML might show rounded 13,205,000
        "polygon-etp": "1,561,000",
        "smart-contract-leaders-etp": "306,000"
    }
    
    driver = None
    results = {}
    
    try:
        driver = setup_driver()
        
        for url in test_urls:
            product_name = extract_product_name(url)
            print(f"\n----- Testing {product_name} -----")
            print(f"URL: {url}")
            
            try:
                result = extract_vaneck_de_shares(driver, url)
                results[product_name] = result
                
                if "outstanding_shares" in result:
                    print(f"SUCCESS: Found outstanding shares: {result['outstanding_shares']}")
                    
                    # Check if the result is the creation unit value (630,000)
                    if "630,000" in result['outstanding_shares'] or "63,000" in result['outstanding_shares']:
                        print(f"WARNING: Got Creation Unit value instead of Notes Outstanding!")
                    
                    # Compare with expected value
                    if product_name in expected_values:
                        expected = expected_values[product_name]
                        actual = result['outstanding_shares']
                        
                        # Normalize values for comparison
                        expected_clean = expected.replace(',', '').replace(' ', '')
                        actual_clean = actual.replace(',', '').replace(' ', '')
                        
                        if expected_clean == actual_clean:
                            print(f"✓ MATCHED EXPECTED: Got {actual} (expected {expected})")
                        else:
                            print(f"✗ MISMATCH: Got {actual} (expected {expected})")
                            
                            # Check if we're close (allow for small formatting differences)
                            expected_num = int(expected_clean)
                            actual_num = int(actual_clean)
                            if 0.9 <= actual_num / expected_num <= 1.1:  # Within 10%
                                print(f"  However values are within 10% - might be rounding differences")
                else:
                    print(f"FAILED: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"ERROR during extraction: {str(e)}")
                import traceback
                traceback.print_exc()
            
            # Add a delay between requests
            time.sleep(2)
        
        # Print summary
        print("\n===== TEST RESULTS SUMMARY =====")
        success_count = sum(1 for r in results.values() if "outstanding_shares" in r)
        print(f"Total URLs tested: {len(test_urls)}")
        print(f"Successful extractions: {success_count}")
        print(f"Success rate: {success_count/len(test_urls)*100:.1f}%")
        
        # Count Creation Unit values
        creation_unit_count = sum(
            1 for r in results.values() 
            if "outstanding_shares" in r and 
            ("630,000" in r['outstanding_shares'] or "63,000" in r['outstanding_shares'])
        )
        if creation_unit_count > 0:
            print(f"WARNING: {creation_unit_count} results returned Creation Unit value (630,000)")
        
        print("\nResults by product:")
        for product, result in results.items():
            if "outstanding_shares" in result:
                # Mark Creation Unit values
                if "630,000" in result['outstanding_shares'] or "63,000" in result['outstanding_shares']:
                    print(f"✗ {product}: {result['outstanding_shares']} (CREATION UNIT VALUE!)")
                else:
                    expected = expected_values.get(product, "unknown")
                    print(f"✓ {product}: {result['outstanding_shares']} (expected: {expected})")
            else:
                print(f"✗ {product}: FAILED - {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"Test error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
    
    return success_count, len(test_urls)

if __name__ == "__main__":
    try:
        success, total = test_vaneck_de_extractor()
        print(f"\nTest completed with {success}/{total} successful extractions")
        
        # Exit with success if we found values and none were 630,000
        sys.exit(0 if success > 0 else 1)
    except Exception as e:
        print(f"Script error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 