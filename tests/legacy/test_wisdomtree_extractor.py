"""
Test script for the WisdomTree extractor

This script tests the custom extractor for wisdomtree.eu URLs to ensure it works
across ALL URLs from this domain, not just specific examples, and handles
multiple language variants including English (en-gb) and German (de-ch, de-de).

REMEMBER: Custom extractors MUST work for ALL URLs from a domain,
not just specific example URLs!
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_wisdomtree_shares

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_wisdomtree_extractor():
    """
    Test the WisdomTree extractor across multiple URLs to ensure it works for ALL wisdomtree.eu URLs,
    not just specific patterns, and handles different language variants.
    """
    # List of test URLs from different parts of wisdomtree.eu, including different language variants
    test_urls = [
        # English (en-gb) URLs
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-coindesk-20",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-crypto-altcoins",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-crypto-market",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-crypto-mega-cap-equal-weight",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-ethereum",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-polkadot",
        "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-xrp",
        
        # German (de-ch) URLs
        "https://www.wisdomtree.eu/de-ch/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-cardano",
        "https://www.wisdomtree.eu/de-ch/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
        
        # German (de-de) URLs
        "https://www.wisdomtree.eu/de-de/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-solana"
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
        print("TESTING WISDOMTREE EXTRACTOR ACROSS MULTIPLE URLs AND LANGUAGE VARIANTS")
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
        
        # Group URLs by language for reporting
        english_urls = [url for url in test_urls if "/en-" in url]
        german_urls = [url for url in test_urls if "/de-" in url]
        
        print(f"Testing {len(english_urls)} English URLs and {len(german_urls)} German URLs")
        
        for url in test_urls:
            # Determine language for reporting
            language = "English" if "/en-" in url else "German"
            product_name = url.split("/")[-1]
            
            print(f"\nTesting URL ({language}): {url}")
            try:
                # Call the WisdomTree extractor directly
                result = extract_wisdomtree_shares(driver, url)
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
            time.sleep(2)
        
        # Print summary
        print("\n" + "=" * 80)
        print(f"SUMMARY: {success_count} successes, {failure_count} failures")
        print("=" * 80)
        
        # Calculate success rates by language
        english_results = {url: result for url, result in results.items() if "/en-" in url}
        german_results = {url: result for url, result in results.items() if "/de-" in url}
        
        english_success = sum(1 for result in english_results.values() if "outstanding_shares" in result)
        german_success = sum(1 for result in german_results.values() if "outstanding_shares" in result)
        
        english_success_rate = (english_success / len(english_urls)) * 100 if english_urls else 0
        german_success_rate = (german_success / len(german_urls)) * 100 if german_urls else 0
        
        print(f"English URL success rate: {english_success_rate:.2f}% ({english_success}/{len(english_urls)})")
        print(f"German URL success rate: {german_success_rate:.2f}% ({german_success}/{len(german_urls)})")
        
        # Print detailed results
        print("\nDETAILED RESULTS:")
        for url, result in results.items():
            language = "English" if "/en-" in url else "German"
            product_name = url.split("/")[-1]
            status = "✅ SUCCESS" if "outstanding_shares" in result else "❌ FAILURE"
            value = result.get("outstanding_shares", result.get("error", "Unknown error"))
            print(f"{status} [{language}]: {product_name} - {value}")
        
        # Calculate overall success rate
        success_rate = (success_count / len(test_urls)) * 100
        print(f"\nOverall success rate: {success_rate:.2f}%")
        
        # Provide feedback based on success rate
        if success_rate == 100:
            print("\n✅ ALL TESTS PASSED! The extractor works for all WisdomTree URLs across all language variants.")
        elif success_rate >= 80:
            print("\n⚠️ MOST TESTS PASSED! The extractor works for most WisdomTree URLs but needs improvement.")
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
                    language = "English" if "/en-" in url else "German"
                    product_name = url.split("/")[-1]
                    print(f"- [{language}] {product_name}")
                    
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
    test_wisdomtree_extractor() 