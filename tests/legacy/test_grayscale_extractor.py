"""
Test script for the Grayscale extractor

This script tests the custom extractor for grayscale.com URLs to ensure it works
across ALL URLs from this domain, not just specific examples, and handles
multiple URL patterns including /funds/, /crypto-products/, and etfs.grayscale.com.

REMEMBER: Custom extractors MUST work for ALL URLs from a domain,
not just specific example URLs!
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_grayscale_shares

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_grayscale_extractor():
    """
    Test the Grayscale extractor across multiple URLs to ensure it works for ALL grayscale.com URLs,
    not just specific patterns, including different URL structures.
    """
    # List of test URLs from different parts of grayscale.com, including different URL patterns
    test_urls = [
        # /funds/ URL pattern
        "https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust",
        "https://www.grayscale.com/funds/grayscale-chainlink-trust",
        "https://www.grayscale.com/funds/grayscale-digital-large-cap-fund",
        "https://www.grayscale.com/funds/grayscale-filecoin-trust",
        "https://www.grayscale.com/funds/grayscale-horizen-trust",
        "https://www.grayscale.com/funds/grayscale-litecoin-trust",
        "https://www.grayscale.com/funds/grayscale-livepeer-trust",
        "https://www.grayscale.com/funds/grayscale-solana-trust",
        "https://www.grayscale.com/funds/grayscale-stellar-lumens-trust",
        "https://www.grayscale.com/funds/grayscale-zcash-trust",
        
        # /crypto-products/ URL pattern
        "https://www.grayscale.com/crypto-products/grayscale-bitcoin-cash-trust",
        "https://www.grayscale.com/crypto-products/grayscale-chainlink-trust",
        "https://www.grayscale.com/crypto-products/grayscale-digital-large-cap-fund",
        "https://www.grayscale.com/crypto-products/grayscale-filecoin-trust",
        "https://www.grayscale.com/crypto-products/grayscale-solana-trust",
        
        # ETF site URL pattern
        "https://etfs.grayscale.com/ethe"
    ]
    
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    
    try:
        print("=" * 80)
        print("TESTING GRAYSCALE EXTRACTOR ACROSS MULTIPLE URL PATTERNS")
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
        
        # Group URLs by pattern for reporting
        funds_urls = [url for url in test_urls if "/funds/" in url]
        crypto_product_urls = [url for url in test_urls if "/crypto-products/" in url]
        etf_urls = [url for url in test_urls if "etfs.grayscale.com" in url]
        
        print(f"Testing {len(funds_urls)} /funds/ URLs, {len(crypto_product_urls)} /crypto-products/ URLs, and {len(etf_urls)} ETF URLs")
        
        for url in test_urls:
            # Determine URL pattern for reporting
            if "/funds/" in url:
                pattern = "funds"
            elif "/crypto-products/" in url:
                pattern = "crypto-products"
            elif "etfs.grayscale.com" in url:
                pattern = "etf"
            else:
                pattern = "other"
                
            product_name = url.split("/")[-1]
            
            print(f"\nTesting URL ({pattern}): {url}")
            try:
                # Call the Grayscale extractor directly
                result = extract_grayscale_shares(driver, url)
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
            
            # Add a short delay between requests to avoid rate limiting
            time.sleep(3)
        
        # Print summary
        print("\n" + "=" * 80)
        print(f"SUMMARY: {success_count} successes, {failure_count} failures")
        print("=" * 80)
        
        # Calculate success rates by URL pattern
        funds_results = {url: result for url, result in results.items() if "/funds/" in url}
        crypto_product_results = {url: result for url, result in results.items() if "/crypto-products/" in url}
        etf_results = {url: result for url, result in results.items() if "etfs.grayscale.com" in url}
        
        funds_success = sum(1 for result in funds_results.values() if "outstanding_shares" in result)
        crypto_product_success = sum(1 for result in crypto_product_results.values() if "outstanding_shares" in result)
        etf_success = sum(1 for result in etf_results.values() if "outstanding_shares" in result)
        
        funds_success_rate = (funds_success / len(funds_urls)) * 100 if funds_urls else 0
        crypto_product_success_rate = (crypto_product_success / len(crypto_product_urls)) * 100 if crypto_product_urls else 0
        etf_success_rate = (etf_success / len(etf_urls)) * 100 if etf_urls else 0
        
        print(f"/funds/ URL success rate: {funds_success_rate:.2f}% ({funds_success}/{len(funds_urls)})")
        print(f"/crypto-products/ URL success rate: {crypto_product_success_rate:.2f}% ({crypto_product_success}/{len(crypto_product_urls)})")
        print(f"ETF URL success rate: {etf_success_rate:.2f}% ({etf_success}/{len(etf_urls)})")
        
        # Print detailed results
        print("\nDETAILED RESULTS:")
        for url, result in results.items():
            if "/funds/" in url:
                pattern = "funds"
            elif "/crypto-products/" in url:
                pattern = "crypto-products"
            elif "etfs.grayscale.com" in url:
                pattern = "etf"
            else:
                pattern = "other"
                
            product_name = url.split("/")[-1]
            status = "✅ SUCCESS" if "outstanding_shares" in result else "❌ FAILURE"
            value = result.get("outstanding_shares", result.get("error", "Unknown error"))
            print(f"{status} [{pattern}]: {product_name} - {value}")
        
        # Calculate overall success rate
        success_rate = (success_count / len(test_urls)) * 100
        print(f"\nOverall success rate: {success_rate:.2f}%")
        
        # Provide feedback based on success rate
        if success_rate == 100:
            print("\n✅ ALL TESTS PASSED! The extractor works for all Grayscale URLs across all URL patterns.")
        elif success_rate >= 80:
            print("\n⚠️ MOST TESTS PASSED! The extractor works for most Grayscale URLs but needs improvement.")
        else:
            print("\n❌ TOO MANY FAILURES! The extractor needs significant improvement.")
            
        print("\nIMPORTANT REMINDER: Custom functions MUST work for ALL URLs from a domain, not just specific patterns!")
        
        # Identify patterns in failures to guide improvements
        if failure_count > 0:
            print("\nFAILURE PATTERN ANALYSIS:")
            # Group failures by error message to identify patterns
            error_groups = {}
            for url, result in results.items():
                if "error" in result:
                    error_msg = result["error"]
                    if error_msg not in error_groups:
                        error_groups[error_msg] = []
                    error_groups[error_msg].append(url)
            
            # Print grouped errors
            for error, urls in error_groups.items():
                print(f"\nError: {error}")
                print("Affected URLs:")
                for url in urls:
                    if "/funds/" in url:
                        pattern = "funds"
                    elif "/crypto-products/" in url:
                        pattern = "crypto-products"
                    elif "etfs.grayscale.com" in url:
                        pattern = "etf"
                    else:
                        pattern = "other"
                    product_name = url.split("/")[-1]
                    print(f"- [{pattern}] {product_name}")
                    
            # Suggest improvements based on failure patterns
            print("\nSUGGESTED IMPROVEMENTS:")
            if any("selector" in err.lower() for err in error_groups.keys()):
                print("- Add more flexible selectors to handle different page layouts")
            if any("timeout" in err.lower() for err in error_groups.keys()):
                print("- Increase wait times or add better wait conditions")
            if any("not found" in err.lower() for err in error_groups.keys()):
                print("- Add more fallback extraction methods")
                
            print("- Test with real browser (non-headless) to inspect failing pages")
            print("- Add more regex patterns to catch different text formats")
            print("- Consider product-specific extraction logic based on URL patterns")
        
    except Exception as e:
        print(f"Test script error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_grayscale_extractor() 