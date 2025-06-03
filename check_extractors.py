#!/usr/bin/env python3
"""
Quick test to check if remaining custom extractors are available
"""

import sys
import os
sys.path.append('src')

print("CHECKING REMAINING CUSTOM EXTRACTORS AVAILABILITY")
print("=" * 60)

# Import the main module
from outstanding_shares_updater import CUSTOM_EXTRACTORS_AVAILABLE, IMPROVED_EXTRACTORS_AVAILABLE

print(f"CUSTOM_EXTRACTORS_AVAILABLE: {CUSTOM_EXTRACTORS_AVAILABLE}")
print(f"IMPROVED_EXTRACTORS_AVAILABLE: {IMPROVED_EXTRACTORS_AVAILABLE}")

# Check if the specific extractors we want to test are available
from custom_domain_extractors import get_custom_extractor

remaining_domains = [
    "lafv.li",
    "augmentasicav.com", 
    "invesco.com",
    "rexshares.com",
    "money.tmx.com"
]

print("\nCHECKING EXTRACTOR AVAILABILITY:")
print("-" * 40)

available_extractors = []
for domain in remaining_domains:
    extractor = get_custom_extractor(domain)
    if extractor:
        print(f"[OK] {domain}: {extractor.__name__}")
        available_extractors.append(domain)
    else:
        print(f"[FAIL] {domain}: No extractor found")

print(f"\nSUMMARY: {len(available_extractors)}/{len(remaining_domains)} extractors available")

# If extractors are available, we can proceed with testing
if available_extractors:
    print(f"[SUCCESS] Ready to test {len(available_extractors)} extractors")
    print("Available for testing:", ", ".join(available_extractors))
else:
    print("[ERROR] No extractors available for testing")
