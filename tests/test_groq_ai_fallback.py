#!/usr/bin/env python3
"""
Test script for Groq AI fallback functionality
Tests the AI analysis on various financial websites
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from excel_stock_updater import try_ai_fallback, analyze_website_with_groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_ai_fallback():
    """Test the AI fallback functionality on various URLs"""
    
    # Test URLs that might be challenging for traditional scraping
    test_urls = [
        # Stock exchanges that might have dynamic content
        "https://www.londonstockexchange.com/exchange/news/market-news/market-news-detail/ETHE/15721358",
        "https://www.cboe.com/us/equities/market_statistics/book/BTCO/",
        "https://www.nasdaq.com/market-activity/stocks/msft",
        
        # Fund/ETF pages
        "https://etfs.grayscale.com/ethe",
        "https://www.proshares.com/our-etfs/strategic/biti",
        
        # European exchanges
        "https://live.euronext.com/en/product/etfs/FR0010524777-XPAR",
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
        
        print("🤖 GROQ AI FALLBACK TESTING")
        print("=" * 50)
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n📊 Test {i}: {url}")
            print("-" * 60)
            
            try:
                result = try_ai_fallback(driver, url)
                
                if "ai extracted price" in result:
                    price = result["ai extracted price"]
                    print(f"✅ SUCCESS: AI extracted price: {price}")
                elif "error" in result:
                    print(f"❌ FAILED: {result['error']}")
                else:
                    print(f"❓ UNKNOWN: {result}")
                    
            except Exception as e:
                print(f"💥 EXCEPTION: {e}")
                
        print(f"\n🏁 Test completed!")
        
    except Exception as e:
        print(f"❌ Driver setup error: {e}")
    finally:
        if driver:
            driver.quit()

def test_ai_analysis_only():
    """Test just the AI analysis function with sample HTML"""
    
    print("\n🧠 TESTING AI ANALYSIS FUNCTION")
    print("=" * 40)
    
    # Sample HTML content that contains a price
    sample_html = """
    <html>
    <head><title>Stock Quote</title></head>
    <body>
        <div class="header">Company XYZ Stock</div>
        <div class="price-section">
            <h2>Current Market Data</h2>
            <div class="share-price">Share Price: $85.42</div>
            <div class="volume">Volume: 1,234,567</div>
            <div class="nav">NAV: $90.15</div>
            <div class="aum">AUM: $1.2B</div>
        </div>
    </body>
    </html>
    """
    
    try:
        result = analyze_website_with_groq(sample_html, "https://example.com/test")
        
        if "ai_extracted_price" in result:
            price = result["ai_extracted_price"]
            print(f"✅ SUCCESS: AI extracted price: {price}")
            print(f"   Expected: 85.42 (should ignore NAV: 90.15)")
        elif "error" in result:
            print(f"❌ FAILED: {result['error']}")
        else:
            print(f"❓ UNKNOWN: {result}")
            
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")

if __name__ == "__main__":
    print("🚀 STARTING GROQ AI FALLBACK TESTS")
    print("This will test the AI's ability to extract share prices from websites")
    print("while avoiding NAV and AUM values.\n")
    
    # Test AI analysis function first
    test_ai_analysis_only()
    
    # Then test full fallback system
    test_ai_fallback()
    
    print("\n✨ All tests completed!") 