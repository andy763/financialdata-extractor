#!/usr/bin/env python3
"""
Simple test for remaining custom domain extractors
"""

import sys
import os
sys.path.append('src')

print("=" * 80)
print("TESTING REMAINING CUSTOM DOMAIN EXTRACTORS")
print("=" * 80)

try:
    from outstanding_shares_updater import (
        extract_outstanding_shares_with_ai_fallback,
        CUSTOM_EXTRACTORS_AVAILABLE,
        IMPROVED_EXTRACTORS_AVAILABLE
    )
    print(f"✅ Imports successful!")
    print(f"CUSTOM_EXTRACTORS_AVAILABLE: {CUSTOM_EXTRACTORS_AVAILABLE}")
    print(f"IMPROVED_EXTRACTORS_AVAILABLE: {IMPROVED_EXTRACTORS_AVAILABLE}")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test cases for remaining domains
test_cases = [
    ("lafv.li", "https://www.lafv.li/de/fonds/list/42585"),
    ("augmentasicav.com", "https://augmentasicav.com/documents"),
    ("invesco.com", "https://www.invesco.com/uk/en/financial-products/etfs/invesco-physical-bitcoin.html"),
    ("rexshares.com", "https://www.rexshares.com/funds/rex-short-bitcoin-strategy-etf/"),
    ("money.tmx.com", "https://money.tmx.com/en/quote/BTCC")
]

results = []
for domain, url in test_cases:
    print(f"\n🔍 Testing {domain}...")
    print(f"URL: {url}")
    
    try:
        result = extract_outstanding_shares_with_ai_fallback(url)
        if result and result.get('outstanding_shares') and result.get('outstanding_shares') != 'N/A':
            shares = result.get('outstanding_shares')
            method = result.get('method', 'unknown')
            print(f"✅ SUCCESS: {shares:,} shares (method: {method})")
            results.append((domain, True, shares, method))
        else:
            print(f"❌ FAILED: No shares extracted")
            results.append((domain, False, None, None))
    except Exception as e:
        print(f"❌ ERROR: {e}")
        results.append((domain, False, None, str(e)))

print("\n" + "=" * 80)
print("FINAL RESULTS SUMMARY")
print("=" * 80)

success_count = 0
custom_count = 0

for domain, success, shares, method in results:
    if success:
        success_count += 1
        if method == 'custom':
            custom_count += 1
        print(f"✅ {domain}: {shares:,} shares (method: {method})")
    else:
        print(f"❌ {domain}: Failed")

print(f"\nSuccess Rate: {success_count}/{len(test_cases)} ({success_count/len(test_cases)*100:.1f}%)")
print(f"Custom Method Usage: {custom_count}/{success_count} successful extractions")

if success_count == len(test_cases):
    print("\n🎉 ALL REMAINING EXTRACTORS WORKING PERFECTLY!")
elif success_count > 0:
    print(f"\n⚠️  {success_count} out of {len(test_cases)} extractors working")
else:
    print("\n❌ NONE of the remaining extractors are working")
