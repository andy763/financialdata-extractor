# Extractor: Financial Data Automation Tool

A comprehensive Python toolkit for extracting stock prices and outstanding shares data from financial websites, with AI-powered fallback capabilities.

## 🔑 Key Features

- **Stock Price Extraction**: Automatically retrieves current stock prices from 17+ exchanges and platforms
- **Outstanding Shares Tracking**: Extracts outstanding shares information from financial websites
- **AI Fallback System**: Uses Groq AI (Llama 3.3) to analyze websites when traditional extraction fails
- **Custom Domain Extractors**: Specialized parsers for challenging websites like Valour, Grayscale, VanEck
- **Excel Integration**: Seamlessly updates Excel spreadsheets with the latest financial data

## 📋 Main Components

- **[excel_stock_updater.py](./excel_stock_updater.py)**: Extracts current stock prices from various financial platforms
- **[outstanding_shares_updater.py](./outstanding_shares_updater.py)**: Retrieves outstanding shares data from company websites
- **[src/custom_domain_extractors.py](./src/custom_domain_extractors.py)**: Domain-specific extraction logic for challenging websites
- **[src/improved_custom_domain_extractors.py](./src/improved_custom_domain_extractors.py)**: Enhanced extraction methods

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/extractor.git
cd extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Chrome/Chromium is installed (required for Selenium)

## 📊 Usage

### Extracting Stock Prices

```bash
python excel_stock_updater.py
```

This will:
- Load URLs from `data/Custodians.xlsx`
- Extract current stock prices from financial websites
- Update `data/Custodians_Results.xlsx` with the latest prices

### Extracting Outstanding Shares

```bash
python outstanding_shares_updater.py
```

This will:
- Load URLs from `data/Custodians.xlsx`
- Extract outstanding shares information
- Update `data/Custodians_Results.xlsx` with the shares data

### Using Batch Files

For Windows users, we provide batch files for easy execution:

```bash
# Run both extractors
batch_files/run_updater_with_shares.bat

# Run stock price extractor only
batch_files/run_updater.bat

# Run shares extractor only
batch_files/run_sixgroup_updater.bat
```

## 📁 Data Structure

- **Input**: `data/Custodians.xlsx` - Main Excel file containing URLs to process
- **Output**: `data/Custodians_Results.xlsx` - Results file with extracted data
- **Excel Structure**:
  - **Column L**: Stock prices
  - **Column M**: Outstanding shares
  - **Column P**: Primary URLs for processing
  - **Column Q**: Fallback URLs (optional)

## 🤖 AI Fallback System

When traditional web scraping methods fail, the system uses Groq's Llama 3.3 AI model to:

- Analyze webpage content intelligently
- Extract specific financial information like share prices and outstanding shares
- Distinguish between different types of financial metrics
- Handle various number formats and currencies
- Results from AI extraction are tagged with "(AI)" for transparency

## 🛠️ Supported Financial Platforms

The system supports extracting data from numerous financial platforms including:

- Börse Frankfurt
- NASDAQ
- Euronext
- TMX
- BX Swiss
- London Stock Exchange
- CBOE US & AU
- VanEck
- Grayscale
- Valour
- WisdomTree
- ProShares
- And many more

## 🧩 Extending the System

### Adding Custom Extractors

To add support for a new financial website:

1. Create a custom extractor function in `src/custom_domain_extractors.py`
2. Register the extractor in the `DOMAIN_EXTRACTORS` dictionary
3. Follow existing extractors as examples for proper pattern matching

### Important Notes for Development

- Custom extractors must work for ALL URLs from a domain, not just specific test cases
- Use robust selectors and fallback mechanisms for maximum reliability
- Test thoroughly with multiple different URLs from the same domain
- Consider all possible page layouts and dynamic content

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Your Name - Initial work and maintenance 