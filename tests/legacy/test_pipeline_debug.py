#!/usr/bin/env python3
"""
Test script to debug the full extraction pipeline for Valour.com
to see if custom extractor results are properly handled by the main function
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging to see detailed information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_pipeline_debug():
    """Test the full extraction pipeline to debug the issue"""
    
    print("🔍 TESTING FULL EXTRACTION PIPELINE")
    print("=" * 60)
    
    # Test URL that we know works with custom extractor
    test_url = "https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd"
    
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        print(f"\n🌐 Testing URL: {test_url}")
        print("-" * 50)
        
        # Import the functions we need to test
        from outstanding_shares_updater import extract_outstanding_shares_with_ai_fallback
        from src.custom_domain_extractors import extract_with_custom_function
        
        # Step 1: Test the custom extractor directly
        print("\n1️⃣ Testing custom extractor directly:")
        try:
            custom_result = extract_with_custom_function(driver, test_url)
            print(f"   Custom extractor result: {custom_result}")
            print(f"   Type: {type(custom_result)}")
            
            if isinstance(custom_result, dict):
                if "outstanding_shares" in custom_result:
                    print("   ✅ Custom extractor returned successful dictionary")
                elif "error" in custom_result:
                    print("   ❌ Custom extractor returned error dictionary")
                else:
                    print("   ⚠️ Custom extractor returned unexpected dictionary")
            elif isinstance(custom_result, str):
                print("   📝 Custom extractor returned string")
            else:
                print(f"   ❓ Custom extractor returned unexpected type: {type(custom_result)}")
                
        except Exception as e:
            print(f"   💥 Custom extractor error: {e}")
        
        # Step 2: Test the full pipeline
        print("\n2️⃣ Testing full extraction pipeline:")
        try:
            full_result = extract_outstanding_shares_with_ai_fallback(driver, test_url)
            print(f"   Full pipeline result: {full_result}")
            print(f"   Type: {type(full_result)}")
            
            if isinstance(full_result, dict):
                if "outstanding_shares" in full_result:
                    print("   ✅ Full pipeline succeeded")
                    method = full_result.get("method", "unknown")
                    print(f"   🔧 Method used: {method}")
                elif "error" in full_result:
                    print("   ❌ Full pipeline failed")
                    error = full_result.get("error", "unknown error")
                    print(f"   💀 Error: {error}")
                    method = full_result.get("method", "unknown")
                    print(f"   🔧 Method attempted: {method}")
                else:
                    print("   ❓ Full pipeline returned unexpected format")
            else:
                print(f"   ❓ Full pipeline returned non-dict: {type(full_result)}")
                
        except Exception as e:
            print(f"   💥 Full pipeline error: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 3: Analysis
        print("\n3️⃣ Analysis:")
        if 'custom_result' in locals() and 'full_result' in locals():
            if (isinstance(custom_result, dict) and "outstanding_shares" in custom_result and 
                isinstance(full_result, dict) and "error" in full_result):
                print("   🚨 BUG DETECTED: Custom extractor succeeded but full pipeline failed!")
                print("   🔍 This confirms the logic issue in extract_outstanding_shares_with_ai_fallback")
            elif (isinstance(custom_result, dict) and "outstanding_shares" in custom_result and 
                  isinstance(full_result, dict) and "outstanding_shares" in full_result):
                print("   ✅ WORKING: Custom extractor succeeded and full pipeline succeeded!")
            else:
                print("   ❓ INCONCLUSIVE: Mixed results or unexpected formats")
        
    except Exception as e:
        print(f"❌ Test setup error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_pipeline_debug()
