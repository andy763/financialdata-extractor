with open('excel_stock_updater.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

start_line = None
end_line = None

# Search for the line with price_keywords definition
for i, line in enumerate(lines):
    if "price_keywords = ['price'" in line:
        start_line = i
    if start_line is not None and "has_price_context = any" in line:
        end_line = i
        break

if start_line is not None and end_line is not None:
    # Replace the price_keywords definition with the fixed version
    fixed_lines = [
        "                price_keywords = ['price', 'share price', 'market price', 'last price', 'trading price', \n",
        "                                'current price', 'last traded', 'closing price', 'nav', 'quote']\n",
        "                has_price_context = any(keyword in context_lower for keyword in price_keywords)\n"
    ]
    
    # Replace the lines
    lines[start_line:end_line+1] = fixed_lines
    
    # Write the modified content back to the file
    with open('excel_stock_updater.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f'Fixed price_keywords list at lines {start_line+1}-{end_line+1}!')
else:
    print('Could not find the price_keywords list in the file.') 