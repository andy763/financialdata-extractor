import requests
import re

def debug_boerse_frankfurt_homepage():
    """Debug the Börse Frankfurt homepage to understand the current structure."""
    
    print("Debugging Börse Frankfurt homepage...")
    print("=" * 50)
    
    try:
        # Get the homepage
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        
        print("Fetching homepage...")
        r = session.get("https://www.boerse-frankfurt.de/", timeout=10)
        r.raise_for_status()
        
        print(f"Status code: {r.status_code}")
        print(f"Content length: {len(r.text)}")
        
        # Look for JavaScript files
        js_files = re.findall(r'src="([^"]*\.js[^"]*)"', r.text)
        print(f"\nFound {len(js_files)} JavaScript files:")
        for js_file in js_files[:10]:  # Show first 10
            print(f"  {js_file}")
        
        # Look for main.*.js specifically
        main_js_matches = re.findall(r'src="(/main\.[^"]*\.js)"', r.text)
        print(f"\nMain JS files found: {len(main_js_matches)}")
        for main_js in main_js_matches:
            print(f"  {main_js}")
        
        # Try alternative patterns
        alt_patterns = [
            r'src="/(main\.[^"]+\.js)"',
            r'src="([^"]*main[^"]*\.js)"',
            r'src="([^"]*bundle[^"]*\.js)"',
            r'src="([^"]*app[^"]*\.js)"'
        ]
        
        print("\nTrying alternative patterns:")
        for pattern in alt_patterns:
            matches = re.findall(pattern, r.text)
            print(f"  Pattern {pattern}: {len(matches)} matches")
            for match in matches[:3]:  # Show first 3
                print(f"    {match}")
        
        # Show a sample of the HTML around script tags
        script_sections = re.findall(r'<script[^>]*src="[^"]*"[^>]*>', r.text)
        print(f"\nFirst 5 script tags:")
        for script in script_sections[:5]:
            print(f"  {script}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_boerse_frankfurt_homepage() 