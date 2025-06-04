import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_tmx_shares

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_tmx_extractor():
    """
    Test the money.tmx.com extractor across multiple URLs to ensure it works for ALL money.tmx.com URLs,
    not just specific patterns
    """
    # List of test URLs from different parts of money.tmx.com
    test_urls = [
        "https://money.tmx.com/en/quote/ETHH.B",
        "https://money.tmx.com/en/quote/BTCC",
        "https://money.tmx.com/en/quote/BTCC.B",
        "https://money.tmx.com/en/quote/BTCC.U",
        "https://money.tmx.com/en/quote/BTCY.B",
        "https://money.tmx.com/en/quote/ETHH",
        "https://money.tmx.com/en/quote/ETHH.U"
    ]
    
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = None
    
    try:
        print("=" * 80)
        print("TESTING MONEY.TMX.COM EXTRACTOR ACROSS MULTIPLE URLs")
        print("CUSTOM FUNCTIONS MUST WORK FOR ALL URLs FROM A DOMAIN, NOT JUST SPECIFIC PATTERNS")
        print("=" * 80)
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        # Test each URL
        results = {}
        success_count = 0
        failure_count = 0
        
        for url in test_urls:
            print(f"\nTesting URL: {url}")
            try:
                result = extract_tmx_shares(driver, url)
                results[url] = result
                
                if "outstanding_shares" in result:
                    success_count += 1
                    print(f"✅ SUCCESS: Found outstanding shares: {result['outstanding_shares']}")
                else:
                    failure_count += 1
                    print(f"❌ FAILURE: {result.get('error', 'Unknown error')}")
            except Exception as e:
                failure_count += 1
                print(f"❌ ERROR: {str(e)}")
                results[url] = {"error": str(e)}
        
        # Print summary
        print("\n" + "=" * 80)
        print(f"SUMMARY: {success_count} successes, {failure_count} failures")
        print("=" * 80)
        
        # Print detailed results
        for url, result in results.items():
            status = "✅ SUCCESS" if "outstanding_shares" in result else "❌ FAILURE"
            value = result.get("outstanding_shares", result.get("error", "Unknown error"))
            print(f"{status}: {url} - {value}")
        
        success_rate = (success_count / len(test_urls)) * 100
        print(f"\nSuccess rate: {success_rate:.2f}%")
        
        if success_count == len(test_urls):
            print("\n✅ ALL TESTS PASSED! The extractor works for all money.tmx.com URLs.")
        else:
            print("\n⚠️ SOME TESTS FAILED! The extractor needs further improvement.")
            
        print("\nIMPORTANT REMINDER: Custom functions MUST work for ALL URLs from a domain, not just specific patterns!")
        
    except Exception as e:
        print(f"Test script error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_tmx_extractor() 