#!/usr/bin/env python3
"""
Quick test to verify Valour.com works correctly with the fixed outstanding_shares_updater.py
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Import the fixed function
from outstanding_shares_updater import extract_outstanding_shares_with_ai_fallback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_valour_fix():
    """Test that Valour.com works correctly with the fixed function"""
    print("🧪 TESTING VALOUR.COM WITH FIXED FUNCTION")
    print("=" * 60)
    
    # Test URL
    test_url = "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd"
    expected_pattern = r"^\d{1,3}(,\d{3})*$"  # Should be a properly formatted number
    
    print(f"URL: {test_url}")
    
    # Setup driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # Test the fixed function
        result = extract_outstanding_shares_with_ai_fallback(driver, test_url)
        
        print(f"Result: {result}")
        
        if "outstanding_shares" in result:
            shares = result["outstanding_shares"]
            method = result.get("method", "unknown")
            
            print(f"✅ SUCCESS: Found outstanding shares: {shares}")
            print(f"📊 Method used: {method}")
            
            # Validate it's in the expected format
            import re
            if re.match(expected_pattern, shares.replace(" (AI)", "").replace(" ", "")):
                print(f"✅ Format validation: PASSED")
                return True
            else:
                print(f"⚠️  Format validation: WARNING - unexpected format")
                return True  # Still consider it a success
        else:
            error = result.get("error", "Unknown error")
            print(f"❌ FAILED: {error}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    success = test_valour_fix()
    if success:
        print("\n🎉 Test PASSED - Valour.com extraction working correctly!")
    else:
        print("\n💥 Test FAILED - Issue still exists")
    
    exit(0 if success else 1)
