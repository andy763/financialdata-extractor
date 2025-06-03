#!/usr/bin/env python
"""
Command-line tool to extract outstanding shares from SIX Group URLs
"""
import sys
import argparse
from .sixgroup_shares_extractor import get_sixgroup_shares_outstanding

def main():
    parser = argparse.ArgumentParser(
        description="Extract outstanding shares from SIX Group URLs",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "urls", 
        nargs="+", 
        help="One or more SIX Group URLs to process"
    )
    
    parser.add_argument(
        "--csv", 
        action="store_true", 
        help="Output in CSV format (URL,Shares)"
    )
    
    args = parser.parse_args()
    
    # Print CSV header if needed
    if args.csv:
        print("URL,Outstanding Shares")
    
    # Process each URL
    for url in args.urls:
        try:
            result = get_sixgroup_shares_outstanding(url)
            
            if args.csv:
                if "error" in result:
                    print(f"{url},ERROR")
                else:
                    print(f"{url},{result['outstanding_shares']}")
            else:
                print(f"\nURL: {url}")
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Outstanding Shares: {result['outstanding_shares']:,}")
                    
        except Exception as e:
            if args.csv:
                print(f"{url},ERROR: {str(e)}")
            else:
                print(f"\nURL: {url}")
                print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main() 