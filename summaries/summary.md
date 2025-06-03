# Stock and Shares Outstanding Data Extractor - Summary

## File Structure & Purpose

### Main Scripts
- **`excel_stock_updater.py`** - Extracts stock prices from various financial websites
- **`outstanding_shares_updater.py`** - Extracts outstanding shares information from company websites
- **`sixgroup_shares_extractor.py`** - Specialized extractor for SIX Group (Swiss Exchange) URLs
- **`sixgroup_cli.py`** - Command-line interface for SIX Group extraction

### Batch Files (Windows)
- **`run_updater_with_shares.bat`** - Runs both stock price and outstanding shares updaters
- **`run_updater.bat`** - Runs only the stock price updater with dependency installation
- **`run_sixgroup_updater.bat`** - Runs only the SIX Group extractor
- **`test_fallback_functionality.bat`** - Tests the fallback URL functionality

### Test Files
- **`test_boerse_frankfurt.py`** - Tests Börse Frankfurt functionality
- **`debug_boerse_frankfurt.py`** - Debugging tool for Börse Frankfurt website changes
- **`test_sixgroup_extractor.py`** - Tests SIX Group extraction
- Various test files for other exchanges (NASDAQ, Euronext, TMX, BX Swiss)

## Data Flow & File Management

### Input File
- **`Custodians.xlsx`** - The main input file containing URLs and data to be processed
  - Column L: Destination for stock prices
  - Column M: Destination for outstanding shares
  - Column P: Primary URLs for processing
  - Column Q: Fallback URLs (optional)

### Output File
- **`Custodians_Results.xlsx`** - All results are saved here
  - This file is automatically created from a fresh copy of `Custodians.xlsx`
  - Original `Custodians.xlsx` remains unchanged

### Data Processing Workflow

#### When Running Individual Scripts:

1. **`excel_stock_updater.py`**:
   - Deletes existing `Custodians_Results.xlsx`
   - Copies `Custodians.xlsx` → `Custodians_Results.xlsx`
   - Processes URLs from column P
   - Saves stock prices to column L in `Custodians_Results.xlsx`

2. **`outstanding_shares_updater.py`**:
   - If `Custodians_Results.xlsx` doesn't exist: copies `Custodians.xlsx` → `Custodians_Results.xlsx`
   - If it exists: uses the existing file (preserving previous results)
   - Processes URLs from column P (with fallback to column Q)
   - Saves outstanding shares to column M in `Custodians_Results.xlsx`

#### When Running Combined Batch File:

**`run_updater_with_shares.bat`**:
1. First runs `excel_stock_updater.py` (creates fresh copy, adds stock prices to column L)
2. Then runs `outstanding_shares_updater.py` (uses existing copy, adds outstanding shares to column M)
   - ✅ **Result**: Both stock prices and outstanding shares in one file

## Exchange Support

### Stock Prices (`excel_stock_updater.py`)
1. **Börse Frankfurt** - Uses official API for "Closing price prev trading day"
2. **NASDAQ** - European market and regular market activity pages
3. **BX Swiss** - Last traded price extraction
4. **Euronext** - Live valuation price extraction
5. **TMX Money** - Share price extraction
6. **Fidelity** - Open price extraction
7. **ProShares ETF** - Market price extraction
8. **Grayscale ETF** - Share price extraction
9. **QR Asset** - Brazilian fund prices
10. **Montpensier Arbével** - French fund prices
11. **Hashdex** - US and Brazil ETF prices
12. **Xtrackers Galaxy** - Bitcoin & Ethereum ETC prices
13. **SIX Group** - Previous close price

### Outstanding Shares (`outstanding_shares_updater.py`)
1. **SIX Group** - Specialized "Number in issue" extraction
2. **Generic** - Keyword-based extraction for any website containing "outstanding" shares information

## Key Features

### Fallback URL Support
- Primary URLs processed from column P
- If extraction fails, automatically tries fallback URL from column Q
- Useful for ensuring data extraction reliability

### Smart Number Parsing
- Handles various number formats (US: 1,234.56, European: 1.234,56)
- Supports space-separated thousands (2 599 000)
- Recognizes magnitude suffixes (million, billion, K, M, B)
- Intelligent decimal/thousand separator detection

### Error Handling
- Comprehensive error logging
- Graceful handling of timeout and network issues
- Automatic browser reset on failures
- Detailed error messages in output cells

### Authentication & Headers
- Börse Frankfurt: Dynamic salt extraction and API authentication
- User-agent spoofing to avoid detection
- Proper timeout handling for slow-loading pages

## Configuration

### File Locations
- Input: `Custodians.xlsx` (preserved, never modified)
- Output: `Custodians_Results.xlsx` (automatically created/overwritten)

### Processing Limits- Max row: 372 (configurable in `excel_stock_updater.py`)- Max row: 500 (configurable in `outstanding_shares_updater.py`)- Processes ALL rows regardless of cell color (orange exclusion removed)

### Browser Settings
- Headless Chrome operation
- 1920x1080 resolution
- Image loading disabled for speed
- Custom user agent for compatibility

## Troubleshooting

### Common Issues
1. **Permission Errors**: Make sure `Custodians_Results.xlsx` is not open in Excel
2. **Browser Issues**: Chrome and ChromeDriver are automatically managed
3. **Network Timeouts**: Configurable timeouts for slow-loading pages
4. **Exchange Changes**: Debug tools available for website structure changes

### Testing- `test_boerse_frankfurt.py` - Test Börse Frankfurt API functionality- `test_fallback_functionality.bat` - Test fallback URL system- Individual exchange test files for debugging specific sites## New Features (Latest Update)### Timestamp Column Headers- Column L1 and M1 headers are automatically updated with timestamp after each run- Format: "Share price (Last updated: 2024-05-24 14:30:15)"- Provides clear indication of when data was last refreshed### Comprehensive Logging System- Individual log files created for each script run- Combined log file created when batch file is used- Error tracking by domain root (e.g., https://www.londonstockexchange.com/)- Success rate statistics (e.g., "199/300 URLs succeeded")- Separate sections for stock prices and outstanding shares errors### Processing Changes- Removed orange cell color exclusion - ALL rows are now processed- More comprehensive coverage of available data- No manual row exclusions needed### Dynamic Row Detection- **Automatic Row Scanning**: No more predetermined row limits (372/500)- **Smart URL Detection**: Automatically finds all rows with valid HTTP/HTTPS URLs in column P- **Complete Coverage**: Processes the entire worksheet regardless of size- **Enhanced Error Tracking**: Improved URL root identification and fallback handling 