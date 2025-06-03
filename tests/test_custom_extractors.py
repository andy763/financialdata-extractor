"""
Test script for custom domain extractors
Tests the new custom extraction functions for high-error domains
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_with_custom_function

def test_custom_extractors():
    """Test custom extractors with sample URLs from each domain"""
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test URLs for each custom extractor
    test_urls = [
        # Valour.com URLs (18 URLs with errors)
        "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd",
        "https://valour.com/en/products/valour-bitcoin-physical-staking",
        
        # VanEck URLs (13 URLs with errors)
        "https://www.vaneck.com/de/en/investments/avalanche-etp/overview/",
        "https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/",
        
        # WisdomTree URLs (11 URLs with errors)
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
        
        # ProShares URLs (10 URLs with errors)
        "https://www.proshares.com/our-etfs/strategic/bito",
        "https://www.proshares.com/our-etfs/leveraged-and-inverse/biti",
        
        # Grayscale URLs (10 URLs with errors)
        "https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust",
        "https://www.grayscale.com/funds/grayscale-chainlink-trust",
        
        # LAFV URLs (10 URLs with errors)
        "https://www.lafv.li/de/fonds/list/42585",
        
        # Augmenta URLs (8 URLs with errors)
        "https://augmentasicav.com/documents",
        
        # Invesco URLs (6 URLs with errors)
        "https://www.invesco.com/uk/en/financial-products/etfs/invesco-physical-bitcoin.html",
        
        # Amina Group URLs (5 URLs with errors)
        "https://aminagroup.com/individuals/investments/btc-usd-tracker-certificate/",
        
        # REX Shares URLs (5 URLs with errors)
        "https://www.rexshares.com/btcl/",
    ]
    
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Disable images to speed up page load
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(30)
        
        print("TESTING CUSTOM DOMAIN EXTRACTORS")
        print("=" * 50)
        
        successful_extractions = 0
        total_tests = len(test_urls)
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n[{i}/{total_tests}] Testing: {url}")
            
            try:
                result = extract_with_custom_function(driver, url)
                
                if "outstanding_shares" in result:
                    print(f"✅ SUCCESS: Found {result['outstanding_shares']} outstanding shares")
                    successful_extractions += 1
                elif "No custom extractor available" in result.get("error", ""):
                    print(f"⚠️  NO CUSTOM EXTRACTOR: {result['error']}")
                else:
                    print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ EXCEPTION: {str(e)}")
        
        print(f"\n" + "=" * 50)
        print(f"SUMMARY:")
        print(f"Total URLs tested: {total_tests}")
        print(f"Successful extractions: {successful_extractions}")
        print(f"Success rate: {successful_extractions/total_tests:.1%}")
        
        if successful_extractions > 0:
            print(f"\n✅ Custom extractors are working! {successful_extractions} successful extractions.")
        else:
            print(f"\n❌ No successful extractions. Custom extractors may need refinement.")
            
    except Exception as e:
        print(f"Test setup error: {e}")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_custom_extractors() 