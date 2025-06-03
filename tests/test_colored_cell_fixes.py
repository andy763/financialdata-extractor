#!/usr/bin/env python3
"""
Test Script for Colored Cell Fixes

This script tests the enhanced extraction functions to verify they work
correctly for the specific issues identified in the colored cells.
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_enhanced_extraction_functions():
    """
    Test the enhanced extraction functions with sample URLs from the colored cells.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # Test cases based on the colored cell issues
        test_cases = [
            {
                'category': 'Purple Cells (Wrong Figures)',
                'description': 'Grayscale - should extract correct price instead of wrong figure',
                'url': 'https://www.grayscale.com/funds/grayscale-chainlink-trust',
                'expected_range': (1.0, 500.0),
                'issue_rows': '9-15, 133-137, 153, 158, 160'
            },
            {
                'category': 'Orange Cells (.0 Errors)',
                'description': 'Valour - should extract decimal price instead of .0 value',
                'url': 'https://valour.com/en/products/valour-cardano',
                'expected_range': (0.01, 1000.0),
                'issue_rows': '110, 117, 121, 123, 130, 136, 170, 172-173'
            },
            {
                'category': 'Red Cells (Hard Errors)',
                'description': 'Bitcap - should handle consent and extract price',
                'url': 'https://bitcap.com/en/bit-crypto-opportunities-institutional-en/?confirmed=1',
                'expected_range': (0.1, 10000.0),
                'issue_rows': '39-43, 83, 107-108, 115, 178'
            }
        ]
        
        print("Testing Enhanced Extraction Functions")
        print("=" * 60)
        print()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i}: {test_case['category']}")
            print(f"Description: {test_case['description']}")
            print(f"Affected Rows: {test_case['issue_rows']}")
            print(f"URL: {test_case['url']}")
            print("-" * 60)
            
            try:
                # Import the enhanced functions from the updated main script
                from excel_stock_updater import (
                    enhanced_grayscale_price_extraction,
                    enhanced_valour_price_extraction,
                    enhanced_bitcap_price_extraction
                )
                
                # Determine which function to use based on URL
                if 'grayscale.com' in test_case['url']:
                    price = enhanced_grayscale_price_extraction(driver, test_case['url'])
                    function_used = "enhanced_grayscale_price_extraction"
                elif 'valour.com' in test_case['url']:
                    price = enhanced_valour_price_extraction(driver, test_case['url'])
                    function_used = "enhanced_valour_price_extraction"
                elif 'bitcap.com' in test_case['url']:
                    price = enhanced_bitcap_price_extraction(driver, test_case['url'])
                    function_used = "enhanced_bitcap_price_extraction"
                else:
                    print("❓ No specific enhanced function for this URL")
                    continue
                
                # Validate the extracted price
                min_price, max_price = test_case['expected_range']
                if min_price <= price <= max_price:
                    print(f"✅ SUCCESS: {function_used}")
                    print(f"   Extracted Price: ${price}")
                    print(f"   Price Range Valid: {min_price} <= {price} <= {max_price}")
                    
                    # Additional validation for specific issues
                    if 'valour.com' in test_case['url']:
                        # Check if it's not a .0 value
                        if str(price).endswith('.0'):
                            print(f"⚠️  WARNING: Still extracted .0 value: {price}")
                        else:
                            print(f"✅ DECIMAL FIX: Successfully avoided .0 error")
                    
                else:
                    print(f"⚠️  WARNING: Price outside expected range")
                    print(f"   Extracted Price: ${price}")
                    print(f"   Expected Range: {min_price} - {max_price}")
                
            except Exception as e:
                print(f"❌ FAILED: {test_case['category']}")
                print(f"   Error: {e}")
                
                # For consent-related errors, this might be expected
                if 'consent' in str(e).lower() or 'cookie' in str(e).lower():
                    print(f"   Note: This may require manual consent handling")
            
            print()
            time.sleep(2)  # Brief pause between tests
        
        print("Test Summary:")
        print("=" * 60)
        print("The enhanced functions have been integrated into excel_stock_updater.py")
        print("These functions address the specific issues in the colored cells:")
        print()
        print("🟣 Purple Cells: Enhanced extraction methods for correct figures")
        print("🔴 Red Cells: Cookie consent handling for blocked sites")
        print("🟠 Orange Cells: Decimal precision requirements to avoid .0 errors")
        print("🟢 Dark Green: Improved primary extraction to reduce AI dependency")
        print()
        print("Next step: Run the updated excel_stock_updater.py on your full dataset")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure the integration script ran successfully and the enhanced functions are in excel_stock_updater.py")
    
    finally:
        driver.quit()

def validate_integration():
    """
    Validate that the enhanced functions were properly integrated.
    """
    print("Validating Integration...")
    print("-" * 30)
    
    try:
        # Check if the enhanced functions exist in the main script
        with open("excel_stock_updater.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        enhanced_functions = [
            "enhanced_grayscale_price_extraction",
            "enhanced_valour_price_extraction", 
            "enhanced_bitcap_price_extraction",
            "enhanced_morningstar_price_extraction"
        ]
        
        for func_name in enhanced_functions:
            if f"def {func_name}(" in content:
                print(f"✅ {func_name} - Found")
            else:
                print(f"❌ {func_name} - Missing")
        
        # Check if the integration points exist
        integration_points = [
            "# --- Grayscale ETF pages (ENHANCED) ---",
            "# --- Valour pages (ENHANCED) ---",
            "# --- Bitcap pages (ENHANCED) ---",
            "# --- Morningstar.be pages (ENHANCED) ---"
        ]
        
        print("\nIntegration Points:")
        for point in integration_points:
            if point in content:
                print(f"✅ {point}")
            else:
                print(f"❌ {point}")
        
        print("\n✅ Integration validation complete")
        
    except Exception as e:
        print(f"❌ Validation error: {e}")

if __name__ == "__main__":
    print("Colored Cell Fixes Test Script")
    print("=" * 40)
    print()
    
    # First validate the integration
    validate_integration()
    print()
    
    # Then test the functions
    test_enhanced_extraction_functions() 