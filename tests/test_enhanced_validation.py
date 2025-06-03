#!/usr/bin/env python3
"""
Test script to verify the enhanced .0 detection logic works correctly
"""

def is_valid_share_price(price_value, context_text="", url=""):
    """
    Comprehensive validation to filter out obvious non-price values.
    Returns True if the value is likely a real share price, False otherwise.
    """
    try:
        price = float(price_value)
        
        # Basic range validation - exclude extremely unreasonable values
        if price <= 0 or price > 100000:
            return False
        
        # ENHANCED .0 DETECTION - Detect ALL forms of .0 values (24.00, 30.0, etc.)
        # Check if the number has only zeros after the decimal point
        price_str = str(price)
        if '.' in price_str:
            # Split into integer and decimal parts
            integer_part, decimal_part = price_str.split('.')
            # Check if decimal part contains only zeros (handles 24.0, 24.00, 24.000, etc.)
            if decimal_part and all(digit == '0' for digit in decimal_part):
                is_zero_decimal = True
                whole_number_value = int(float(price))  # Convert to int for further checks
            else:
                is_zero_decimal = False
                whole_number_value = None
        else:
            # It's already a whole number (no decimal point)
            is_zero_decimal = True
            whole_number_value = int(price)
        
        # If it's a .0 value (including 24.00, 30.0, etc.), apply strict filtering
        if is_zero_decimal and whole_number_value is not None:
            print(f"  🔍 Detected .0 value: {price} -> whole number: {whole_number_value}")
            # For this test, we'll return False for ALL .0 values to flag them
            return False
        
        # For non-.0 values, be more permissive
        print(f"  ✅ Valid decimal value: {price}")
        return True
        
    except (ValueError, TypeError):
        return False

def test_validation():
    """Test various price values to verify .0 detection"""
    
    test_cases = [
        # .0 values that should be flagged
        (24.0, "Should be flagged as .0"),
        (24.00, "Should be flagged as .0"),
        (30.0, "Should be flagged as .0"),
        (5.0, "Should be flagged as .0"),
        (100.0, "Should be flagged as .0"),
        (1.0, "Should be flagged as .0"),
        (2025.0, "Should be flagged as .0 (year)"),
        
        # Valid decimal values that should NOT be flagged
        (24.37, "Valid decimal - should NOT be flagged"),
        (1.0092, "Valid decimal - should NOT be flagged"),
        (30.15, "Valid decimal - should NOT be flagged"),
        (5.99, "Valid decimal - should NOT be flagged"),
        (100.25, "Valid decimal - should NOT be flagged"),
        (16.64, "Valid decimal - should NOT be flagged"),
        (44.59, "Valid decimal - should NOT be flagged"),
        (3.01, "Valid decimal - should NOT be flagged"),
        
        # Edge cases
        (0.5, "Valid small decimal"),
        (0.01, "Valid very small decimal"),
        (999.99, "Valid large decimal"),
    ]
    
    print("🧪 Testing Enhanced .0 Detection Logic")
    print("=" * 60)
    
    flagged_count = 0
    valid_count = 0
    
    for price, description in test_cases:
        print(f"\nTesting: {price} ({description})")
        is_valid = is_valid_share_price(price)
        
        if is_valid:
            print(f"  ✅ VALID: {price}")
            valid_count += 1
        else:
            print(f"  🚫 FLAGGED: {price}")
            flagged_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY:")
    print(f"{'='*60}")
    print(f"Total tests: {len(test_cases)}")
    print(f"Flagged as invalid: {flagged_count}")
    print(f"Marked as valid: {valid_count}")
    
    # Expected results
    expected_flagged = 7  # All the .0 values
    expected_valid = len(test_cases) - expected_flagged
    
    print(f"\n🎯 EXPECTED:")
    print(f"Should flag: {expected_flagged} (.0 values)")
    print(f"Should allow: {expected_valid} (decimal values)")
    
    if flagged_count == expected_flagged and valid_count == expected_valid:
        print(f"\n✅ TEST PASSED! Logic working correctly.")
    else:
        print(f"\n❌ TEST FAILED! Logic needs adjustment.")
        print(f"Expected {expected_flagged} flagged, got {flagged_count}")
        print(f"Expected {expected_valid} valid, got {valid_count}")

if __name__ == "__main__":
    test_validation() 