import sys
import logging

# Test if all imports work
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup
    import re
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Simple test
def simple_test():
    print("Starting simple TradingView test...")
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        url = "https://www.tradingview.com/symbols/NASDAQ-ZZZ/"
        print(f"Navigating to: {url}")
        
        driver.get(url)
        print("Page loaded successfully!")
        
        # Get page title
        title = driver.title
        print(f"Page title: {title}")
        
        # Check if we can find any price-related elements
        page_source = driver.page_source
        print(f"Page source length: {len(page_source)}")
        
        # Look for common price patterns
        price_patterns = [
            r'\$\s*([\d,]+\.[\d]{2})',
            r'([\d,]+\.[\d]{2})\s*USD',
            r'"price":\s*"?([\d,]+\.[\d]{2})"?'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, page_source)
            if matches:
                print(f"Found price matches with pattern {pattern}: {matches[:5]}")  # Show first 5
        
        driver.quit()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
