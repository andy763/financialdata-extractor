"""
Simple test script to verify basic functionality
"""

import sys
import platform
import requests
import traceback

def test_basic_connection():
    """Test basic connectivity and environment"""
    try:
        print("\n===== BASIC CONNECTIVITY TEST =====\n")
        
        # Print Python and environment info
        print(f"Python version: {sys.version}")
        print(f"Platform: {platform.platform()}")
        
        # Test simple web request
        print("\nTesting web connectivity...")
        response = requests.get("https://www.google.com", timeout=5)
        print(f"Google response: {response.status_code}")
        
        # Test VanEck website
        print("\nTesting VanEck website connectivity...")
        response = requests.get("https://www.vaneck.com", timeout=10)
        print(f"VanEck response: {response.status_code}")
        
        print("\nBasic connectivity test passed!")
        return True
    except Exception as e:
        print(f"Error in basic connectivity test: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_connection() 