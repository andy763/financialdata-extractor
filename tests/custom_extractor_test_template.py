"""
Template for testing custom domain extractors

USAGE:
1. Copy this file and rename to test_[domain]_extractor.py
2. Replace placeholder values with your domain-specific information
3. Add at least 5-7 different URLs from the domain for thorough testing
4. Run the test to verify domain-wide compatibility

REMEMBER: Custom extractors MUST work for ALL URLs from a domain,
not just specific example URLs!
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.custom_domain_extractors import extract_with_custom_function

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_domain_extractor():
    """
    Test the [DOMAIN] extractor across multiple URLs to ensure it works for ALL [DOMAIN] URLs,
    not just specific patterns
    """
    # List of test URLs from different parts of [DOMAIN]
    # IMPORTANT: Include at least 5-7 different URLs with various layouts/patterns
    test_urls = [
        "https://[DOMAIN]/section1/page1",
        "https://[DOMAIN]/section1/page2",
        "https://[DOMAIN]/section2/page1",
        "https://[DOMAIN]/section3/different-layout",
        "https://[DOMAIN]/section4/another-pattern",
        # Add more URLs to ensure thorough testing
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
        print("TESTING [DOMAIN] EXTRACTOR ACROSS MULTIPLE URLs")
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
                # Either call your specific extractor function directly:
                # result = extract_domain_shares(driver, url)
                
                # Or use the general extractor function:
                result = extract_with_custom_function(driver, url)
                
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
        
        # Print detailed results
        for url, result in results.items():
            status = "✅ SUCCESS" if "outstanding_shares" in result else "❌ FAILURE"
            value = result.get("outstanding_shares", result.get("error", "Unknown error"))
            print(f"{status}: {url} - {value}")
        
        # Calculate success rate
        success_rate = (success_count / len(test_urls)) * 100
        print(f"\nSuccess rate: {success_rate:.2f}%")
        
        # Provide feedback based on success rate
        if success_rate == 100:
            print("\n✅ ALL TESTS PASSED! The extractor works for all [DOMAIN] URLs.")
        elif success_rate >= 80:
            print("\n⚠️ MOST TESTS PASSED! The extractor works for most [DOMAIN] URLs but needs improvement.")
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
                    print(f"- {url}")
                    
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
            print("- Consider section-specific extraction logic based on URL patterns")
        
    except Exception as e:
        print(f"Test script error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_domain_extractor() 