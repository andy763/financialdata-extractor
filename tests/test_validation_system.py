#!/usr/bin/env python3
"""
Test script to verify the enhanced price validation system
Tests against real prices and known problematic values from the most recent run
"""

import sys
import os

# Add the main directory to path so we can import the validation function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import is_valid_share_price

def test_validation_system():
    """Test the enhanced validation against real world examples"""
    
    print("🧪 TESTING ENHANCED PRICE VALIDATION SYSTEM")
    print("=" * 60)
    
    # Test cases based on real data from the search results
    test_cases = [
        # VALID PRICES (should return True)
        {
            "price": 23.15,
            "context": "WisdomTree Physical Bitcoin price EUR",
            "url": "https://www.wisdomtree.eu/en-gb/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
            "expected": True,
            "description": "WisdomTree Bitcoin ETF actual price (€23.15)"
        },
        {
            "price": 25.46,
            "context": "Calamos Bitcoin Structured Alt Protection ETF share price",
            "url": "https://www.calamos.com/funds/etf/calamos-bitcoin-structured-alt-protection-etf-january-cboj/",
            "expected": True,
            "description": "Calamos CBOJ actual price ($25.46)"
        },
        {
            "price": 38.89,
            "context": "Simplify US Equity PLUS Bitcoin Strategy ETF NAV",
            "url": "https://www.simplify.us/etfs/spbc-simplify-us-equity-plus-bitcoin-strategy-etf",
            "expected": True,
            "description": "Simplify SPBC actual NAV ($38.89)"
        },
        {
            "price": 47.14,
            "context": "Roundhill Bitcoin Covered Call Strategy ETF price",
            "url": "https://www.dividend.com/etfs/ybtc-roundhill-bitcoin-covered-call-strategy-etf/",
            "expected": True,
            "description": "YBTC actual price ($47.14)"
        },
        
        # INVALID PRICES - Years (should return False)
        {
            "price": 2024.0,
            "context": "Inception date 2024",
            "url": "https://www.wisdomtree.eu/en-gb/products/cryptocurrency/",
            "expected": False,
            "description": "Year value (2024) - should be rejected"
        },
        {
            "price": 2019.0,
            "context": "Launch date 2019",
            "url": "https://www.calamos.com/funds/etf/",
            "expected": False,
            "description": "Year value (2019) - should be rejected"
        },
        
        # INVALID PRICES - Protection percentages (should return False)
        {
            "price": 80.0,
            "context": "80% protection level downside protection",
            "url": "https://www.calamos.com/funds/etf/calamos-bitcoin-80-series-structured-alt-protection-etf-january-cbtj/",
            "expected": False,
            "description": "Calamos 80% protection level - should be rejected"
        },
        {
            "price": 90.0,
            "context": "90% protection downside protection level",
            "url": "https://www.calamos.com/funds/etf/calamos-bitcoin-90-series-structured-alt-protection-etf-january-cbxj/",
            "expected": False,
            "description": "Calamos 90% protection level - should be rejected"
        },
        {
            "price": 100.0,
            "context": "100% protection level full protection",
            "url": "https://www.calamos.com/funds/etf/calamos-bitcoin-structured-alt-protection-etf-january-cboj/",
            "expected": False,
            "description": "Calamos 100% protection level - should be rejected"
        },
        
        # INVALID PRICES - Fund metadata (should return False)
        {
            "price": 1089.0,
            "context": "Fund size EUR 1,089 m assets under management",
            "url": "https://www.wisdomtree.eu/de-ch/products/ucits-etfs-unleveraged-etps/cryptocurrency/wisdomtree-physical-bitcoin",
            "expected": False,
            "description": "WisdomTree fund size (1,089m EUR) - should be rejected"
        },
        {
            "price": 112.0,
            "context": "Fund size 112m AUM assets under management",
            "url": "https://augmentasicav.com/documents",
            "expected": False,
            "description": "Common crypto ETF fund size - should be rejected"
        },
        
        # INVALID PRICES - Version numbers/ratings (should return False)
        {
            "price": 1.0,
            "context": "Version 1.0 rating stars",
            "url": "https://www.nasdaq.com/market-activity/etf/ibit/real-time",
            "expected": False,
            "description": "Version/rating number (1.0) - should be rejected"
        },
        {
            "price": 2.0,
            "context": "Rating 2 stars",
            "url": "https://www.21shares-funds.com/product/arka",
            "expected": False,
            "description": "Rating number (2.0) - should be rejected"
        },
        
        # EDGE CASES - Borderline values
        {
            "price": 0.35,
            "context": "Expense ratio 0.35% TER total expense ratio",
            "url": "https://www.franklintempleton.com/",
            "expected": False,
            "description": "Expense ratio (0.35%) - should be rejected due to context"
        },
        {
            "price": 1576.0,
            "context": "Fund Size in m € (AuM) 1,576",
            "url": "https://www.justetf.com/en/etf-profile.html?isin=GB00BLD4ZL17",
            "expected": False,
            "description": "Large fund size - should be rejected"
        },
        
        # VALID EDGE CASES - Should pass despite being whole numbers
        {
            "price": 15.0,
            "context": "Current trading price market price last price",
            "url": "https://www.vaneck.com/us/en/investments/bitcoin-etf-hodl/",
            "expected": True,
            "description": "Valid whole number price (15.0) with price context"
        },
        {
            "price": 25.0,
            "context": "Share price last traded price",
            "url": "https://www.ishares.com/us/products/bitcoin-trust-etf",
            "expected": True,
            "description": "Valid whole number price (25.0) with price context"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        result = is_valid_share_price(
            test["price"], 
            test["context"], 
            test["url"]
        )
        
        status = "✅ PASS" if result == test["expected"] else "❌ FAIL"
        if result == test["expected"]:
            passed += 1
        else:
            failed += 1
            
        print(f"\nTest {i:2d}: {status}")
        print(f"         Price: {test['price']}")
        print(f"         Expected: {test['expected']}, Got: {result}")
        print(f"         Description: {test['description']}")
        
        if result != test["expected"]:
            print(f"         Context: {test['context'][:100]}...")
            print(f"         URL: {test['url'][:80]}...")
    
    print("\n" + "=" * 60)
    print(f"🎯 TEST RESULTS: {passed} PASSED, {failed} FAILED")
    print(f"📊 SUCCESS RATE: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! The validation system is working correctly.")
    else:
        print("⚠️  Some tests failed. Review the validation logic.")
    
    return failed == 0

if __name__ == "__main__":
    success = test_validation_system()
    exit(0 if success else 1) 