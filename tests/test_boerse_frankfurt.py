import logging
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from excel_stock_updater import _extract_isin_bf, get_prev_close_boerse, fetch_and_extract_data

def test_boerse_frankfurt_urls():
    """Test Börse Frankfurt URLs with expected closing prices."""
    
    # Test data: URL and expected closing price
    test_urls = [
        ("https://www.boerse-frankfurt.de/en/etf/bitwise-ethereum-staking-etp?currency=EUR", 4.6364),
        ("https://www.boerse-frankfurt.de/en/etf/bitwise-msci-digital-assets-select-20-etp?currency=EUR", 118.34),
        ("https://www.boerse-frankfurt.de/en/etf/de000a27z304-etc-issuance-gmbh-0-000?currency=EUR", 87.475)
    ]
    
    print("Testing Börse Frankfurt closing price extraction...")
    print("=" * 60)
    
    for i, (url, expected_price) in enumerate(test_urls, 1):
        print(f"\nTest {i}: {url}")
        print(f"Expected closing price: {expected_price}")
        
        try:
            # Step 1: Extract ISIN
            print("Step 1: Extracting ISIN...")
            isin = _extract_isin_bf(url)
            print(f"Extracted ISIN: {isin}")
            
            # Step 2: Get closing price using API
            print("Step 2: Fetching closing price...")
            closing_price = get_prev_close_boerse(isin)
            print(f"API closing price: {closing_price}")
            
            # Step 3: Compare with expected
            difference = abs(closing_price - expected_price)
            tolerance = 0.01  # Allow small differences due to timing
            
            if difference <= tolerance:
                print(f"✅ SUCCESS: Price matches expected value (difference: {difference:.4f})")
            else:
                print(f"⚠️  WARNING: Price differs from expected (difference: {difference:.4f})")
                print(f"   This might be due to timing or market changes.")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            
        print("-" * 40)
    
    print("\nTesting complete!")

def test_fetch_and_extract_data():
    """Test the full fetch_and_extract_data function with Börse Frankfurt URLs."""
    
    test_urls = [
        "https://www.boerse-frankfurt.de/en/etf/bitwise-ethereum-staking-etp?currency=EUR",
        "https://www.boerse-frankfurt.de/en/etf/bitwise-msci-digital-assets-select-20-etp?currency=EUR",
        "https://www.boerse-frankfurt.de/en/etf/de000a27z304-etc-issuance-gmbh-0-000?currency=EUR"
    ]
    
    print("\nTesting fetch_and_extract_data function...")
    print("=" * 60)
    
    keywords = ["closing price prev trading day"]
    
    for i, url in enumerate(test_urls, 1):
        print(f"\nTest {i}: {url}")
        
        try:
            # Use None for driver since Börse Frankfurt uses API, not Selenium
            result = fetch_and_extract_data(None, url, keywords)
            print(f"Result: {result}")
            
            if "closing price prev trading day" in result:
                print(f"✅ SUCCESS: Got closing price: {result['closing price prev trading day']}")
            elif "error" in result:
                print(f"❌ ERROR: {result['error']}")
            else:
                print(f"⚠️  WARNING: Unexpected result format")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            
        print("-" * 40)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Run tests
    test_boerse_frankfurt_urls()
    test_fetch_and_extract_data() 