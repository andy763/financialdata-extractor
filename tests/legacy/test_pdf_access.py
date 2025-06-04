"""
Simple test script to verify we can access and parse VanEck PDF files.
"""

import requests
import re
import sys
import traceback

def test_pdf_access():
    """Test direct access to PDF files"""
    print("\n===== TESTING PDF ACCESS =====\n")
    
    # Sample PDF URLs for testing
    pdf_urls = [
        "https://www.vaneck.com/de/en/library/fact-sheets/vava-fact-sheet.pdf",  # Avalanche
        "https://www.vaneck.com/de/en/library/fact-sheets/vbtc-fact-sheet.pdf",  # Bitcoin
        "https://www.vaneck.com/de/en/library/fact-sheets/vpol-fact-sheet.pdf",  # Polygon
        "https://www.vaneck.com/de/en/library/fact-sheets/vlnk-fact-sheet.pdf"   # Chainlink
    ]
    
    success_count = 0
    
    for pdf_url in pdf_urls:
        try:
            product_name = pdf_url.split('/')[-1].split('-fact-sheet')[0]
            print(f"\n----- Testing {product_name} PDF -----")
            
            print(f"Downloading: {pdf_url}")
            response = requests.get(pdf_url, timeout=30)
            
            if response.status_code == 200:
                pdf_content = response.content
                pdf_size = len(pdf_content)
                print(f"PDF download successful - size: {pdf_size:,} bytes")
                
                # Check if PDF contains basic terms
                has_notes = b'Notes' in pdf_content
                has_outstanding = b'Outstanding' in pdf_content
                has_combined = b'Notes Outstanding' in pdf_content
                
                print(f"Contains 'Notes': {has_notes}")
                print(f"Contains 'Outstanding': {has_outstanding}")
                print(f"Contains exact phrase 'Notes Outstanding': {has_combined}")
                
                # Look for the term "Notes Outstanding" and nearby numbers
                if has_combined:
                    notes_pos = pdf_content.find(b'Notes Outstanding')
                    print(f"'Notes Outstanding' found at position {notes_pos}")
                    
                    # Get a chunk of text around the term
                    chunk_size = 200
                    chunk_start = max(0, notes_pos - 20)
                    chunk_end = min(pdf_size, notes_pos + chunk_size)
                    chunk = pdf_content[chunk_start:chunk_end]
                    
                    # Show bytes around the term
                    print(f"Chunk around 'Notes Outstanding' (raw bytes):")
                    print(chunk)
                    
                    # Try to find a number in this chunk
                    number_match = re.search(rb'Notes Outstanding[^0-9]*([0-9][0-9,\. ]{3,})', chunk)
                    if number_match:
                        shares_str = number_match.group(1).decode('utf-8', errors='ignore')
                        print(f"Found shares value near 'Notes Outstanding': {shares_str}")
                        success_count += 1
                    else:
                        print("Could not find a number pattern after 'Notes Outstanding'")
                        
                        # Try a wider search for any numbers in the chunk
                        all_numbers = re.findall(rb'([0-9][0-9,\. ]{3,})', chunk)
                        if all_numbers:
                            print(f"Found {len(all_numbers)} number(s) in the chunk:")
                            for i, num in enumerate(all_numbers[:5]):
                                print(f"  #{i+1}: {num.decode('utf-8', errors='ignore')}")
                
                # If we didn't find "Notes Outstanding", search for "Notes" alone
                elif has_notes:
                    print("Searching for 'Notes' with numbers nearby...")
                    notes_positions = []
                    start = 0
                    while True:
                        pos = pdf_content.find(b'Notes', start)
                        if pos == -1:
                            break
                        notes_positions.append(pos)
                        start = pos + 5
                    
                    print(f"Found 'Notes' at {len(notes_positions)} positions")
                    
                    # Check first few "Notes" occurrences
                    for i, pos in enumerate(notes_positions[:3]):
                        chunk_start = max(0, pos - 10)
                        chunk_end = min(pdf_size, pos + 100)
                        chunk = pdf_content[chunk_start:chunk_end]
                        print(f"\nNotes occurrence #{i+1} at position {pos}:")
                        print(chunk)
                        
                        # Look for numbers near this occurrence
                        numbers = re.findall(rb'([0-9][0-9,\. ]{3,})', chunk)
                        if numbers:
                            print(f"Found {len(numbers)} numbers near this 'Notes':")
                            for j, num in enumerate(numbers[:3]):
                                print(f"  #{j+1}: {num.decode('utf-8', errors='ignore')}")
                
                # Simple fallback: just look for large numbers in the PDF
                if not success_count:
                    print("\nFallback: searching for large numbers in PDF...")
                    large_numbers = re.findall(rb'([0-9][0-9,\. ]{5,})', pdf_content)
                    if large_numbers:
                        print(f"Found {len(large_numbers)} large numbers:")
                        for i, num in enumerate(large_numbers[:10]):
                            num_str = num.decode('utf-8', errors='ignore')
                            print(f"  #{i+1}: {num_str}")
                            
                            # Try to clean and see if it's in the right range
                            try:
                                cleaned = num_str.replace('.', '').replace(',', '').replace(' ', '')
                                value = int(cleaned)
                                if 100000 <= value <= 20000000:
                                    print(f"    ✓ Potential share count: {value:,}")
                            except:
                                pass
            else:
                print(f"Failed to download PDF, status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error processing PDF {pdf_url}: {str(e)}")
            traceback.print_exc()
    
    print(f"\nTest complete. Successfully found 'Notes Outstanding' in {success_count}/{len(pdf_urls)} PDFs")
    return success_count

if __name__ == "__main__":
    try:
        test_pdf_access()
    except Exception as e:
        print(f"Script error: {str(e)}")
        traceback.print_exc()
        sys.exit(1) 