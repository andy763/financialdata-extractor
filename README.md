# Financial Data Extractor

This project collects up‑to‑date outstanding share counts and stock prices for a list of exchange traded products. Results are saved to `data/Custodians_Results.xlsx`.

## Quick Start

```bash
pip install -r requirements.txt
python outstanding_shares_updater.py
python excel_stock_updater.py
```

On Windows you can run `batch_files/run_updater_with_shares.bat` to execute both scripts sequentially.

## Directory Layout

```
.
├── excel_stock_updater.py          # price updater
├── outstanding_shares_updater.py   # shares updater
├── src/                            # core scraping modules
├── tests/                          # test suite and legacy scripts
├── data/                           # input workbook and results
├── logs/                           # generated log files
├── html_debug/                     # saved HTML for troubleshooting
├── docs/                           # additional documentation
├── summaries/                      # development summaries
└── batch_files/                    # helper batch scripts
```

## Requirements

- Python 3.10+
- Google Chrome (used by Selenium)

Install the Python dependencies with `pip install -r requirements.txt`.

## Running

The updaters read from `data/Custodians.xlsx` and write results to `data/Custodians_Results.xlsx`. Ensure that Chrome is installed and accessible on your system. Each script logs its progress under the `logs/` directory.

## Testing

All tests live under the `tests/` directory. Many require network access and a working Chrome installation. Example legacy scripts are also kept alongside the tests for reference.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
 