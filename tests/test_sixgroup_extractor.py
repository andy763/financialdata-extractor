"""
Test script for SIX Group shares outstanding extractor
"""
from src.sixgroup_shares_extractor import get_sixgroup_shares_outstanding

def main():
    # Test URLs with known share counts
    test_urls = [
        "https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH1146882316USD4.html#/",
        "https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH0496454155USD4.html#/",
        "https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH0475552201USD4.html#/"
    ]
    
    expected_values = {
        "CH1146882316USD4": 535000,     # 535'000
        "CH0496454155USD4": 14420000,   # 14'420'000
        "CH0475552201USD4": 722703      # 722'703
    }
    
    print("\nTesting SIX Group shares outstanding extractor...")
    print("-" * 60)
    
    success_count = 0
    total_count = len(test_urls)
    
    for url in test_urls:
        # Extract ISIN from URL for reporting
        isin = url.split(".")[-2]
        print(f"Testing {isin}: {url}")
        
        # Get the expected value for this ISIN
        expected = expected_values.get(isin, "Unknown")
        
        # Run the extractor
        result = get_sixgroup_shares_outstanding(url)
        
        if "error" in result:
            print(f"❌ Failed: {result['error']}")
        else:
            shares = result["outstanding_shares"]
            print(f"Found: {shares:,}")
            
            if expected != "Unknown" and shares == expected:
                print(f"✅ Success: Value matches expected {expected:,}")
                success_count += 1
            elif expected != "Unknown":
                print(f"❌ Error: Expected {expected:,} but got {shares:,}")
            else:
                print("⚠️ Warning: No expected value to compare against")
                
        print("-" * 60)
    
    # Print summary
    print(f"Test Summary: {success_count}/{total_count} tests passed")

if __name__ == "__main__":
    main() 