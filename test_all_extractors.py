#!/usr/bin/env python3
"""
Comprehensive test for all custom domain extractors with outstanding_shares_updater.py
Tests: valour.com, wisdomtree.eu, grayscale.com, aminagroup.com, vaneck.com, and others
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

def test_all_custom_extractors():
    """Test all custom domain extractors with the actual outstanding_shares_updater.py"""
    
    # Import the functions from outstanding_shares_updater
    from outstanding_shares_updater import (
        extract_outstanding_shares_with_ai_fallback,
        CUSTOM_EXTRACTORS_AVAILABLE,
        IMPROVED_EXTRACTORS_AVAILABLE
    )
    
    print("=" * 100)
    print("COMPREHENSIVE TEST - ALL CUSTOM DOMAIN EXTRACTORS")
    print(f"CUSTOM_EXTRACTORS_AVAILABLE: {CUSTOM_EXTRACTORS_AVAILABLE}")
    print(f"IMPROVED_EXTRACTORS_AVAILABLE: {IMPROVED_EXTRACTORS_AVAILABLE}")
    print("=" * 100)
    
    # Test cases organized by domain
    test_cases = {
        "valour.com": [
            "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd",
            "https://valour.com/en/products/valour-bitcoin-physical-staking",
            "https://valour.com/en/products/valour-ethereum-physical-staking"
        ],
        "wisdomtree.eu": [
            "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
            "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-ethereum",
            "https://www.wisdomtree.eu/de-ch/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-cardano"
        ],
        "grayscale.com": [
            "https://www.grayscale.com/funds/grayscale-bitcoin-cash-trust",
            "https://www.grayscale.com/funds/grayscale-chainlink-trust",
            "https://www.grayscale.com/crypto-products/grayscale-digital-large-cap-fund"
        ],
        "vaneck.com": [
            "https://www.vaneck.com/us/en/investments/bitcoin-etf-hodl/",
            "https://www.vaneck.com/us/en/investments/ethereum-etf-ethv/"
        ],
        "vaneck.com/de": [
            "https://www.vaneck.com/de/en/institutional/ucits/vaneck-bitcoin-etf/",
            "https://www.vaneck.com/de/en/institutional/ucits/vaneck-ethereum-etf/"
        ],
        "proshares.com": [
            "https://www.proshares.com/funds/bito.html",
            "https://www.proshares.com/funds/bitq.html"
        ],
        "aminagroup.com": [
            "https://www.aminagroup.com/en/funds/digital-assets/amina-bitcoin-etp/",
            "https://www.aminagroup.com/en/funds/digital-assets/amina-ethereum-etp/"
        ]
    }
    
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = None
    total_tests = 0
    total_success = 0
    domain_results = {}
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        print("\nRunning comprehensive tests...")
        print("=" * 100)
        
        for domain, urls in test_cases.items():
            print(f"\n🔍 TESTING DOMAIN: {domain}")
            print("-" * 60)
            
            domain_success = 0
            domain_total = len(urls)
            domain_results[domain] = {"success": 0, "total": domain_total, "results": []}
            
            for i, url in enumerate(urls, 1):
                total_tests += 1
                print(f"\n[{i}/{domain_total}] Testing: {url}")
                
                try:
                    result = extract_outstanding_shares_with_ai_fallback(driver, url)
                    
                    if result and 'outstanding_shares' in result:
                        shares = result['outstanding_shares']
                        method = result.get('method', 'unknown')
                        
                        print(f"✅ SUCCESS: {shares} (method: {method})")
                        
                        # Check for potential bugs (like the 120000 issue)
                        if ("120000" in str(shares) or "120,000" in str(shares)) and domain == "valour.com":
                            # For valour.com, 120,000 might be legitimate for some products
                            if "physical-bitcoin-carbon-neutral-usd" in url:
                                print("   ℹ️  Note: 120,000 might be correct for this specific product")
                            else:
                                print("   ⚠️  Warning: 120,000 might indicate the old bug")
                        
                        domain_success += 1
                        total_success += 1
                        domain_results[domain]["results"].append({"url": url, "shares": shares, "method": method, "status": "success"})
                        
                    else:
                        error_msg = result.get('error', 'No result') if result else 'No result'
                        print(f"❌ FAILED: {error_msg}")
                        domain_results[domain]["results"].append({"url": url, "error": error_msg, "status": "failed"})
                        
                except Exception as e:
                    print(f"❌ ERROR: {e}")
                    domain_results[domain]["results"].append({"url": url, "error": str(e), "status": "error"})
            
            domain_results[domain]["success"] = domain_success
            success_rate = (domain_success / domain_total) * 100 if domain_total > 0 else 0
            
            print(f"\n📊 {domain} Results: {domain_success}/{domain_total} ({success_rate:.1f}%)")
            
            if domain_success == domain_total:
                print(f"🎉 {domain} - ALL TESTS PASSED!")
            elif domain_success > 0:
                print(f"⚠️ {domain} - PARTIAL SUCCESS")
            else:
                print(f"💥 {domain} - ALL TESTS FAILED!")
        
        # Final comprehensive summary
        print("\n" + "=" * 100)
        print("FINAL COMPREHENSIVE RESULTS")
        print("=" * 100)
        
        overall_success_rate = (total_success / total_tests) * 100 if total_tests > 0 else 0
        print(f"Overall Success Rate: {total_success}/{total_tests} ({overall_success_rate:.1f}%)")
        
        print("\nDomain-by-Domain Summary:")
        print("-" * 60)
        
        for domain, results in domain_results.items():
            success_rate = (results["success"] / results["total"]) * 100 if results["total"] > 0 else 0
            status_emoji = "🎉" if results["success"] == results["total"] else "⚠️" if results["success"] > 0 else "💥"
            print(f"{status_emoji} {domain:<20} {results['success']:>2}/{results['total']:>2} ({success_rate:>5.1f}%)")
        
        print("\nDetailed Results by Domain:")
        print("-" * 60)
        
        for domain, results in domain_results.items():
            print(f"\n{domain}:")
            for result in results["results"]:
                if result["status"] == "success":
                    print(f"  ✅ {result['shares']} ({result['method']})")
                else:
                    print(f"  ❌ {result.get('error', 'Unknown error')}")
        
        # Check for critical issues
        print("\n" + "=" * 100)
        print("CRITICAL ISSUES CHECK")
        print("=" * 100)
        
        critical_issues = []
        
        # Check if all valour.com URLs return the same value (the old bug)
        valour_results = domain_results.get("valour.com", {}).get("results", [])
        valour_shares = [r.get("shares") for r in valour_results if r.get("status") == "success"]
        if len(set(valour_shares)) == 1 and len(valour_shares) > 1:
            critical_issues.append(f"⚠️ All valour.com URLs return the same value: {valour_shares[0]}")
        
        # Check for domains with 0% success rate
        failed_domains = [domain for domain, results in domain_results.items() if results["success"] == 0]
        if failed_domains:
            critical_issues.append(f"💥 Domains with 0% success: {', '.join(failed_domains)}")
        
        if critical_issues:
            print("CRITICAL ISSUES FOUND:")
            for issue in critical_issues:
                print(f"  {issue}")
        else:
            print("✅ No critical issues detected!")
        
        print("=" * 100)
            
    except Exception as e:
        print(f"Setup error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_all_custom_extractors()
