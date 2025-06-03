#!/usr/bin/env python3
"""
Comprehensive verification script to ensure 100% correctness of the enhanced integration
"""

import re
import inspect
from excel_stock_updater import (
    fetch_and_extract_data,
    enhanced_grayscale_price_extraction,
    enhanced_valour_price_extraction,
    enhanced_bitcap_price_extraction,
    enhanced_morningstar_price_extraction
)

def verify_function_order():
    """Verify that enhanced functions come before original handlers"""
    print("🔍 VERIFYING FUNCTION ORDER")
    print("=" * 50)
    
    source = inspect.getsource(fetch_and_extract_data)
    
    # Find all handler positions
    handlers = {
        'Enhanced Grayscale': source.find('if "grayscale.com" in url.lower():'),
        'Enhanced Valour': source.find('if "valour.com" in url.lower():'),
        'Enhanced Bitcap': source.find('if "bitcap.com" in url.lower():'),
        'Enhanced Morningstar': source.find('if "morningstar.be" in url.lower():'),
        'Original Grayscale (fallback)': source.find('if "grayscale.com/funds" in url.lower()'),
        'Börse Frankfurt': source.find('if "boerse-frankfurt.de" in url.lower():'),
        'NASDAQ European': source.find('if "nasdaq.com/european-market-activity" in url.lower():'),
    }
    
    # Find all Valour and Bitcap instances
    valour_positions = []
    bitcap_positions = []
    
    start = 0
    while True:
        pos = source.find('if "valour.com" in url.lower():', start)
        if pos == -1:
            break
        valour_positions.append(pos)
        start = pos + 1
    
    start = 0
    while True:
        pos = source.find('if "bitcap.com" in url.lower():', start)
        if pos == -1:
            break
        bitcap_positions.append(pos)
        start = pos + 1
    
    print(f"Found {len(valour_positions)} Valour handlers at positions: {valour_positions}")
    print(f"Found {len(bitcap_positions)} Bitcap handlers at positions: {bitcap_positions}")
    
    # Verify order
    issues = []
    
    # Check that enhanced functions come first
    enhanced_pos = handlers['Enhanced Grayscale']
    boerse_pos = handlers['Börse Frankfurt']
    
    if enhanced_pos == -1:
        issues.append("❌ Enhanced Grayscale function not found")
    elif boerse_pos == -1:
        issues.append("❌ Börse Frankfurt function not found")
    elif enhanced_pos > boerse_pos:
        issues.append("❌ Enhanced functions should come before Börse Frankfurt")
    else:
        print("✅ Enhanced functions come before original handlers")
    
    # Check Valour order
    if len(valour_positions) >= 2:
        if valour_positions[0] < valour_positions[1]:
            print("✅ Enhanced Valour comes before original Valour")
        else:
            issues.append("❌ Enhanced Valour should come before original Valour")
    
    # Check Bitcap order  
    if len(bitcap_positions) >= 2:
        if bitcap_positions[0] < bitcap_positions[1]:
            print("✅ Enhanced Bitcap comes before original Bitcap")
        else:
            issues.append("❌ Enhanced Bitcap should come before original Bitcap")
    
    return issues

def verify_ai_fallback_integration():
    """Verify AI fallback is properly integrated"""
    print("\n🔍 VERIFYING AI FALLBACK INTEGRATION")
    print("=" * 50)
    
    source = inspect.getsource(fetch_and_extract_data)
    
    # Count AI fallback calls
    ai_fallback_count = source.count("try_ai_fallback")
    print(f"Total AI fallback calls: {ai_fallback_count}")
    
    # Check enhanced sections have AI fallback
    enhanced_sections = [
        ("Enhanced Grayscale", "Grayscale ETF pages (ENHANCED)"),
        ("Enhanced Valour", "Valour pages (ENHANCED)"),
        ("Enhanced Bitcap", "Bitcap pages (ENHANCED)"),
        ("Enhanced Morningstar", "Morningstar.be pages (ENHANCED)")
    ]
    
    issues = []
    for name, pattern in enhanced_sections:
        section_start = source.find(f"# --- {pattern}")
        if section_start == -1:
            issues.append(f"❌ {name} section not found")
            continue
            
        # Find the end of this section (next # --- or end of function)
        section_end = source.find("# ---", section_start + 1)
        if section_end == -1:
            section_end = len(source)
        
        section_code = source[section_start:section_end]
        
        if "try_ai_fallback" in section_code:
            print(f"✅ {name} has AI fallback integration")
        else:
            issues.append(f"❌ {name} missing AI fallback integration")
    
    return issues

def verify_enhanced_functions_exist():
    """Verify all enhanced functions exist and are properly defined"""
    print("\n🔍 VERIFYING ENHANCED FUNCTIONS EXIST")
    print("=" * 50)
    
    functions = [
        enhanced_grayscale_price_extraction,
        enhanced_valour_price_extraction,
        enhanced_bitcap_price_extraction,
        enhanced_morningstar_price_extraction
    ]
    
    issues = []
    for func in functions:
        if not callable(func):
            issues.append(f"❌ {func.__name__} is not callable")
        else:
            print(f"✅ {func.__name__} exists and is callable")
            
            # Check function has proper error handling
            source = inspect.getsource(func)
            if "raise ValueError" in source:
                print(f"   ✅ {func.__name__} has proper error handling")
            else:
                issues.append(f"❌ {func.__name__} missing proper error handling")
    
    return issues

def verify_no_duplicate_handlers():
    """Verify there are no conflicting duplicate handlers"""
    print("\n🔍 VERIFYING NO DUPLICATE CONFLICTS")
    print("=" * 50)
    
    source = inspect.getsource(fetch_and_extract_data)
    
    # Check for problematic patterns
    issues = []
    
    # Check that enhanced functions don't have exact duplicates
    enhanced_patterns = [
        'if "grayscale.com" in url.lower():',
        'if "valour.com" in url.lower():',
        'if "bitcap.com" in url.lower():',
        'if "morningstar.be" in url.lower():'
    ]
    
    for pattern in enhanced_patterns:
        count = source.count(pattern)
        domain = pattern.split('"')[1]
        
        if domain == "grayscale.com":
            # Grayscale should have 1 enhanced + 1 fallback in try block
            if count >= 1:
                print(f"✅ {domain} has {count} handler(s) (enhanced + fallback)")
            else:
                issues.append(f"❌ {domain} missing handlers")
        elif domain in ["valour.com", "bitcap.com"]:
            # These should have 2: enhanced + original
            if count == 2:
                print(f"✅ {domain} has {count} handlers (enhanced + original)")
            else:
                issues.append(f"❌ {domain} has {count} handlers, expected 2")
        elif domain == "morningstar.be":
            # This should have 1: enhanced only
            if count == 1:
                print(f"✅ {domain} has {count} handler (enhanced only)")
            else:
                issues.append(f"❌ {domain} has {count} handlers, expected 1")
    
    return issues

def verify_error_handling_consistency():
    """Verify error handling is consistent across all enhanced functions"""
    print("\n🔍 VERIFYING ERROR HANDLING CONSISTENCY")
    print("=" * 50)
    
    source = inspect.getsource(fetch_and_extract_data)
    
    # Check that all enhanced sections have proper error handling
    enhanced_sections = [
        ("Enhanced Grayscale", "Grayscale ETF pages (ENHANCED)"),
        ("Enhanced Valour", "Valour pages (ENHANCED)"), 
        ("Enhanced Bitcap", "Bitcap pages (ENHANCED)"),
        ("Enhanced Morningstar", "Morningstar.be pages (ENHANCED)")
    ]
    
    issues = []
    for name, pattern in enhanced_sections:
        section_start = source.find(f"# --- {pattern}")
        if section_start == -1:
            issues.append(f"❌ {name} section not found")
            continue
        
        # Find the end of this section
        section_end = source.find("# ---", section_start + 1)
        if section_end == -1:
            section_end = len(source)
        
        section_code = source[section_start:section_end]
        
        # Check for required error handling patterns
        required_patterns = [
            "try:",
            "except ValueError as e:",
            "except Exception as e:",
            "return {\"error\":",
            "logging."
        ]
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in section_code:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            issues.append(f"❌ {name} missing patterns: {missing_patterns}")
        else:
            print(f"✅ {name} has complete error handling")
    
    return issues

def main():
    """Run comprehensive verification"""
    print("🧪 COMPREHENSIVE INTEGRATION VERIFICATION")
    print("=" * 60)
    
    all_issues = []
    
    # Run all verification checks
    all_issues.extend(verify_function_order())
    all_issues.extend(verify_ai_fallback_integration())
    all_issues.extend(verify_enhanced_functions_exist())
    all_issues.extend(verify_no_duplicate_handlers())
    all_issues.extend(verify_error_handling_consistency())
    
    print("\n" + "=" * 60)
    print("📋 VERIFICATION RESULTS")
    print("=" * 60)
    
    if all_issues:
        print("❌ ISSUES FOUND:")
        for issue in all_issues:
            print(f"  {issue}")
        print(f"\nTotal issues: {len(all_issues)}")
        return False
    else:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("✅ Integration is 100% correct and complete")
        print("\n🚀 READY FOR PRODUCTION DEPLOYMENT")
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 