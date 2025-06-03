"""
Test script for the improved VanEck DE extractor
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.improved_custom_domain_extractors import extract_vaneck_de_shares, get_custom_extractor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of VanEck DE URLs to test
VANECK_DE_URLS = [
    "https://www.vaneck.com/de/en/investments/avalanche-etp/overview/",
    "https://www.vaneck.com/de/en/investments/algorand-etp/overview/",
    "https://www.vaneck.com/de/en/investments/chainlink-etp/overview/",
    "https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/",
    "https://www.vaneck.com/de/en/investments/crypto-leaders-etp/overview/",
    "https://www.vaneck.com/de/en/investments/ethereum-etp/overview/",
    "https://www.vaneck.com/de/en/investments/polkadot-etp/overview/",
    "https://www.vaneck.com/de/en/investments/pyth-etp/overview/",
    "https://www.vaneck.com/de/en/investments/smart-contract-leaders-etp/overview/",
    "https://www.vaneck.com/de/en/investments/sui-etp/overview/",
    "https://www.vaneck.com/de/en/investments/tron-etp/overview/",
    "https://www.vaneck.com/de/en/investments/polygon-etp/overview/",
    "https://www.vaneck.com/de/en/investments/solana-etp/overview/"
]

def test_vaneck_de_extractor():
    """Test the VanEck DE extractor on all URLs"""
    
    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    # Add user agent to avoid detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        print("\n" + "="*80)
        print("TESTING VANECK DE EXTRACTOR")
        print("="*80)
        
        results = {
            "success": 0,
            "failed": 0,
            "details": {}
        }
        
        # Test each URL
        for idx, url in enumerate(VANECK_DE_URLS, 1):
            print(f"\n{idx}. Testing URL: {url}")
            
            # Test 1: Check if get_custom_extractor correctly identifies this as a VanEck DE URL
            extractor = get_custom_extractor(url)
            if extractor == extract_vaneck_de_shares:
                print("[PASS] URL correctly identified as VanEck DE")
            else:
                print("[FAIL] URL NOT identified as VanEck DE")
                results["failed"] += 1
                results["details"][url] = {"error": "URL detection failed"}
                continue
            
            # Test 2: Try to extract outstanding shares
            try:
                shares = extract_vaneck_de_shares(driver, url)
                
                if shares:
                    print(f"[PASS] Successfully extracted shares: {shares}")
                    results["success"] += 1
                    results["details"][url] = {"shares": shares}
                else:
                    print("[FAIL] Could not extract shares (returned None)")
                    results["failed"] += 1
                    results["details"][url] = {"error": "No shares found"}
            except Exception as e:
                print(f"[FAIL] Error extracting shares: {str(e)}")
                results["failed"] += 1
                results["details"][url] = {"error": str(e)}
            
            # Add a pause to avoid rate limiting
            time.sleep(2)
        
        # Print summary
        print("\n" + "="*80)
        print("TEST RESULTS SUMMARY")
        print("="*80)
        print(f"Total URLs tested: {len(VANECK_DE_URLS)}")
        print(f"Successful extractions: {results['success']}")
        print(f"Failed extractions: {results['failed']}")
        success_rate = (results['success'] / len(VANECK_DE_URLS)) * 100
        print(f"Success rate: {success_rate:.2f}%")
        
        # Print details of extracted shares
        print("\n" + "="*80)
        print("EXTRACTED SHARES DETAILS")
        print("="*80)
        for url, data in results["details"].items():
            product_name = url.split('/investments/')[1].split('/')[0]
            if "shares" in data:
                print(f"{product_name}: {data['shares']}")
            else:
                print(f"{product_name}: FAILED - {data.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_vaneck_de_extractor() 