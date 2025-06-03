"""
Test script for improved custom domain extractors
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.improved_custom_domain_extractors import extract_with_custom_function

def test_improved_extractors():
    """Test the improved custom extractors with real URLs"""
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test URLs from the investigation
    test_urls = [
        "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd",
        "https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust",
        "https://www.vaneck.com/de/en/investments/bitcoin-etp/overview/",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
        "https://www.proshares.com/our-etfs/strategic/bito",
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
    successful_extractions = 0
    total_tests = len(test_urls)
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(30)
        
        print("=" * 60)
        print("TESTING IMPROVED CUSTOM EXTRACTORS")
        print("=" * 60)
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n[{i}/{total_tests}] Testing: {url}")
            
            try:
                driver.get(url)
                time.sleep(2)  # Brief pause
                
                # Test the improved extractor
                result = extract_with_custom_function(driver, url)
                
                if result:
                    print(f"✅ SUCCESS: Found outstanding shares: {result}")
                    successful_extractions += 1
                else:
                    print(f"❌ FAILED: Could not extract outstanding shares")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
            
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print("SUMMARY:")
        print(f"Total URLs tested: {total_tests}")
        print(f"Successful extractions: {successful_extractions}")
        print(f"Success rate: {(successful_extractions/total_tests)*100:.1f}%")
        
        if successful_extractions > 0:
            print(f"✅ Improved extractors are working!")
        else:
            print(f"❌ No successful extractions. Extractors need further refinement.")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error setting up driver: {str(e)}")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_improved_extractors() 