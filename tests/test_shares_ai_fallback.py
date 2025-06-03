#!/usr/bin/env python3
"""
Test script for Groq AI fallback functionality for outstanding shares
Tests the AI analysis on various financial websites
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from outstanding_shares_updater import extract_outstanding_shares_with_ai_fallback, analyze_shares_with_groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_shares_ai_fallback():
    """Test the AI fallback functionality for outstanding shares on various URLs"""
    
    # Test URLs that might be challenging for traditional scraping
    test_urls = [
        # ETF/Fund pages that might have outstanding shares info
        "https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf",
        "https://investor.vanguard.com/etf/profile/VTI",
        "https://www.spdr.com/en/us/products/spy/",
        
        # Company pages that might have shares outstanding
        "https://investor.apple.com/investor-relations/",
        "https://www.microsoft.com/en-us/investor/",
        
        # Complex fund pages
        "https://etfs.grayscale.com/btc",
    ]
    
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(30)
        
        print("🤖 GROQ AI OUTSTANDING SHARES FALLBACK TESTING")
        print("=" * 60)
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n📊 Test {i}: {url}")
            print("-" * 70)
            
            try:
                result = extract_outstanding_shares_with_ai_fallback(driver, url)
                
                if "outstanding_shares" in result:
                    shares = result["outstanding_shares"]
                    if "(AI)" in shares:
                        print(f"✅ AI SUCCESS: Outstanding shares: {shares}")
                    else:
                        print(f"✅ TRADITIONAL SUCCESS: Outstanding shares: {shares}")
                elif "error" in result:
                    print(f"❌ FAILED: {result['error']}")
                else:
                    print(f"❓ UNKNOWN: {result}")
                    
            except Exception as e:
                print(f"💥 EXCEPTION: {e}")
                
        print(f"\n🏁 Outstanding shares AI test completed!")
        
    except Exception as e:
        print(f"❌ Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

def test_shares_ai_analysis_only():
    """Test just the AI analysis function with sample HTML for outstanding shares"""
    
    print("\n🧠 TESTING OUTSTANDING SHARES AI ANALYSIS FUNCTION")
    print("=" * 50)
    
    # Sample HTML content that contains outstanding shares
    sample_html = """
    <html>
    <head><title>Company ABC Investor Relations</title></head>
    <body>
        <div class="header">Company ABC</div>
        <div class="financial-info">
            <h2>Share Information</h2>
            <div class="outstanding-shares">Outstanding Shares: 150.5 million</div>
            <div class="market-cap">Market Cap: $25.2 billion</div>
            <div class="float">Float: 140.2 million shares</div>
            <div class="volume">Daily Volume: 2.1 million</div>
        </div>
    </body>
    </html>
    """
    
    try:
        result = analyze_shares_with_groq(sample_html, "https://example.com/test")
        
        if "ai_extracted_shares" in result:
            shares = result["ai_extracted_shares"]
            print(f"✅ SUCCESS: AI extracted shares: {shares}")
            print(f"   Expected: Should convert 150.5 million to actual number")
        elif "error" in result:
            print(f"❌ FAILED: {result['error']}")
        else:
            print(f"❓ UNKNOWN: {result}")
            
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")

if __name__ == "__main__":
    print("🚀 STARTING GROQ AI OUTSTANDING SHARES FALLBACK TESTS")
    print("This will test the AI's ability to extract outstanding shares from websites")
    print("and automatically add (AI) tags when AI is used.\n")
    
    # Test AI analysis function first
    test_shares_ai_analysis_only()
    
    # Then test full fallback system
    test_shares_ai_fallback()
    
    print("\n✨ All outstanding shares AI tests completed!") 