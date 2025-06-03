# Stock Prices and Outstanding Shares Logging Tool

This tool allows you to generate log files for stock prices and outstanding shares without having to run the full web scraping process. It analyzes the current state of the Excel file and produces logs in the same format as the main update scripts.

## Requirements

- Python 3.6+
- openpyxl (included in requirements.txt)

## Usage

### Using the Batch File (Windows)

The easiest way to use the logging tool is with the batch file:

```
generate_logs.bat [log_type] [excel_file_path]
```

Where:
- `log_type` is one of:
  - `stock` - Generate stock prices log
  - `shares` - Generate outstanding shares log
  - `combined` - Generate both logs and combine them
- `excel_file_path` is optional. If not provided, it defaults to `custodians.xlsx` in the current directory.

Examples:
```
generate_logs.bat stock
generate_logs.bat shares
generate_logs.bat combined path/to/custodians.xlsx
```

### Using Python Directly

You can also run the Python script directly:

```
python src/generate_logs.py [log_type] [excel_file_path]
```

With the same parameters as described above.

## Output

The logs will be generated in the `logs` directory with the following naming convention:
- Stock prices logs: `stock_prices_log_YYYYMMDD_HHMMSS.txt`
- Outstanding shares logs: `outstanding_shares_log_YYYYMMDD_HHMMSS.txt`
- Combined logs: `combined_extraction_log_YYYYMMDD_HHMMSS.txt`

## Log Format

The generated logs follow the same format as those produced by the main update scripts:

### Stock Prices Log

- Header section with run date and script name
- Error section showing domains with errors, ranked by most errors first
- Invalid price values section
- Blue cells section (cells excluded from success rate)
- Normal cells section (used for success rate)
- Summary section with overall statistics

### Outstanding Shares Log

- Header section with run date and script name
- Error section showing domains with errors
- Summary section with overall statistics

### Combined Log

A combined log includes both the stock prices and outstanding shares logs in a single file.

## How It Works

The tool analyzes the Excel file and determines:
1. Which cells have values vs. which cells have errors
2. Which cells are "blue cells" (excluded from success rate)
3. Which values appear to be invalid (for stock prices)

It then generates logs with the same structure and statistics as the main update scripts.

## Notes

- The tool does not modify the Excel file in any way.
- No web requests are made - all data is derived from the current state of the Excel file.
- The success rates and statistics are based on the presence or absence of values in the appropriate cells. 