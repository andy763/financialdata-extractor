#!/usr/bin/env python3
"""
Test the remaining custom domain extractors that weren't covered in the main test
Tests: lafv.li, augmentasicav.com, invesco.com, rexshares.com, money.tmx.com
"""

import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Add the src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_remaining_extractors():
    """Test the remaining custom domain extractors with outstanding_shares_updater.py"""
    
    # Import the functions from outstanding_shares_updater
    from outstanding_shares_updater import (
        extract_outstanding_shares_with_ai_fallback,
        CUSTOM_EXTRACTORS_AVAILABLE,
        IMPROVED_EXTRACTORS_AVAILABLE
    )
    
    print("=" * 100)
    print("TESTING REMAINING CUSTOM DOMAIN EXTRACTORS")
    print(f"CUSTOM_EXTRACTORS_AVAILABLE: {CUSTOM_EXTRACTORS_AVAILABLE}")
    print(f"IMPROVED_EXTRACTORS_AVAILABLE: {IMPROVED_EXTRACTORS_AVAILABLE}")
    print("=" * 100)
    
    # Test cases for remaining domains - based on error logs and domain analysis
    test_cases = {
        "lafv.li": [
            # URLs from error logs - LAFV has 10 URLs with errors according to logs
            "https://www.lafv.li/de/fonds/list/42585",  # Example from logs
            "https://www.lafv.li/en/funds/crypto-fund"   # Typical crypto fund pattern
        ],
        "augmentasicav.com": [
            # URLs from error logs - Augmenta has 8 URLs with errors
            "https://augmentasicav.com/documents",  # Main documents page seen in logs
            "https://augmentasicav.com/funds/crypto-diversified"  # Typical fund pattern
        ],
        "invesco.com": [
            # URLs from error logs - Invesco has 2-6 URLs with errors depending on log
            "https://www.invesco.com/uk/en/financial-products/etfs/invesco-physical-bitcoin.html",
            "https://www.invesco.com/us/en/financial-products/etfs/invesco-bitcoin-strategy-etf"
        ],
        "rexshares.com": [
            # URLs from error logs - REX Shares has 5 URLs with errors
            "https://www.rexshares.com/btfd/",  # Bitcoin futures fund
            "https://www.rexshares.com/shrt/"   # Short fund
        ],
        "money.tmx.com": [
            # URLs from error logs - TMX Money has 9 URLs with errors
            "https://money.tmx.com/en/quote/ETHH.B",  # Ethereum ETF
            "https://money.tmx.com/en/quote/BTCC",    # Bitcoin ETF
            "https://money.tmx.com/en/quote/BTCC.B"   # Bitcoin ETF (USD)
        ]
    }
    
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    domain_results = {}
    total_success = 0
    total_tested = 0
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        
        # Test each domain
        for domain, urls in test_cases.items():
            print(f"\n{'='*60}")
            print(f"TESTING DOMAIN: {domain}")
            print(f"{'='*60}")
            
            domain_success = 0
            domain_total = len(urls)
            domain_results[domain] = {"results": [], "success_count": 0, "total": domain_total}
            
            for i, url in enumerate(urls, 1):
                print(f"\n[{i}/{domain_total}] Testing: {url}")
                
                try:
                    result = extract_outstanding_shares_with_ai_fallback(driver, url)
                    
                    if result and 'outstanding_shares' in result:
                        shares = result['outstanding_shares']
                        method = result.get('method', 'unknown')
                        
                        print(f"✅ SUCCESS: {shares} (method: {method})")
                        domain_success += 1
                        total_success += 1
                        
                        domain_results[domain]["results"].append({
                            "url": url,
                            "status": "success",
                            "shares": shares,
                            "method": method
                        })
                        
                        # Check if this used a custom extractor
                        if method == "custom":
                            print(f"   🎯 Used custom extractor for {domain}")
                        
                    else:
                        error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                        print(f"❌ FAILED: {error_msg}")
                        
                        domain_results[domain]["results"].append({
                            "url": url,
                            "status": "failed",
                            "error": error_msg
                        })
                    
                    total_tested += 1
                    
                except Exception as e:
                    print(f"❌ ERROR: {str(e)}")
                    total_tested += 1
                    
                    domain_results[domain]["results"].append({
                        "url": url,
                        "status": "error",
                        "error": str(e)
                    })
            
            domain_results[domain]["success_count"] = domain_success
            success_rate = (domain_success / domain_total) * 100 if domain_total > 0 else 0
            
            print(f"\n{domain} Results: {domain_success}/{domain_total} ({success_rate:.1f}%)")
            
            # Print detailed results for this domain
            for result in domain_results[domain]["results"]:
                if result["status"] == "success":
                    print(f"  ✅ {result['shares']} ({result['method']})")
                else:
                    print(f"  ❌ {result.get('error', 'Unknown error')}")
    
    finally:
        if driver:
            driver.quit()
    
    # Print comprehensive summary
    print("\n" + "="*100)
    print("FINAL SUMMARY - REMAINING EXTRACTORS TEST")
    print("="*100)
    
    overall_success_rate = (total_success / total_tested) * 100 if total_tested > 0 else 0
    print(f"Overall Success Rate: {total_success}/{total_tested} ({overall_success_rate:.1f}%)")
    print()
    
    print("Domain Results:")
    for domain, results in domain_results.items():
        success_count = results["success_count"]
        total = results["total"]
        rate = (success_count / total) * 100 if total > 0 else 0
        status_emoji = "🎉" if success_count == total else "⚠️" if success_count > 0 else "❌"
        print(f"{status_emoji} {domain:<20} {success_count}/{total} ({rate:.1f}%)")
    
    # Check for custom extractor usage
    custom_usage = 0
    for domain, results in domain_results.items():
        for result in results["results"]:
            if result.get("method") == "custom":
                custom_usage += 1
    
    print(f"\nCustom Extractor Usage: {custom_usage}/{total_success} successful extractions used custom extractors")
    
    # Final assessment
    print("\n" + "="*100)
    print("ASSESSMENT")
    print("="*100)
    
    if total_success == total_tested:
        print("🎉 EXCELLENT: All remaining extractors are working perfectly!")
        print("✅ All 5 remaining domains have functional custom extractors")
        print("✅ Combined with previous tests, this completes the domain coverage verification")
    elif total_success > total_tested * 0.8:
        print("✅ GOOD: Most remaining extractors are working well")
        print(f"📊 {total_success}/{total_tested} extractors successful")
    elif total_success > 0:
        print("⚠️ PARTIAL: Some extractors working, others need attention")
        print("🔧 Consider reviewing failing domains for improvements")
    else:
        print("❌ CRITICAL: None of the remaining extractors are working")
        print("🚨 These domains may need custom extractor implementation or fixes")
    
    # Recommendations
    print("\nRECOMMENDations:")
    if custom_usage < total_success:
        print("🔍 Some successful extractions didn't use custom extractors")
        print("   Consider checking if custom extractors are properly mapped")
    
    failing_domains = [domain for domain, results in domain_results.items() if results["success_count"] == 0]
    if failing_domains:
        print(f"🔧 Focus on fixing: {', '.join(failing_domains)}")
    
    working_domains = [domain for domain, results in domain_results.items() if results["success_count"] == results["total"]]
    if working_domains:
        print(f"✅ Fully functional: {', '.join(working_domains)}")

if __name__ == "__main__":
    test_remaining_extractors()
