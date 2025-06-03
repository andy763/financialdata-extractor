# Custom Extractors Checker

A powerful Python CLI tool and library for verifying and testing the availability of custom domain extractors in financial data scraping pipelines.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Example Output](#example-output)
- [Directory Structure](#directory-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

Custom Extractors Checker ensures that all your domain-specific extractor modules are properly registered and ready before you run full data extraction jobs. This pre-validation step saves time by catching missing or misconfigured extractors early in development or CI/CD pipelines.

## Features

- Validates presence of both standard and improved extractor sets
- Supports custom domain extractors for multiple financial websites
- Clear, color-coded CLI output for quick diagnosis
- Easily scriptable for automated pipelines

## Prerequisites

- Python 3.8 or later
- Git
- (Optional) Virtual environment (venv, virtualenv) for dependency isolation

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/andy763/extractor2.git
   cd extractor2
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows PowerShell
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

If you maintain extractor modules in a custom location, update the `PYTHONPATH` or modify the `sys.path.append` call in `check_extractors.py` to include your extractor directory.

## Usage

### Basic Usage

Run the checker to verify extractor availability:

```bash
python check_extractors.py
```

### Example Output

```plaintext
CHECKING REMAINING CUSTOM EXTRACTORS AVAILABILITY
============================================================
CUSTOM_EXTRACTORS_AVAILABLE: True
IMPROVED_EXTRACTORS_AVAILABLE: True

CHECKING EXTRACTOR AVAILABILITY:
----------------------------------------
[OK] lafv.li: LAFVExtractor
[OK] augmentasicav.com: AugmentasiCAVExtractor
[FAIL] invesco.com: No extractor found
[OK] rexshares.com: RexSharesExtractor
[OK] money.tmx.com: TMXMoneyExtractor

SUMMARY: 4/5 extractors available
[SUCCESS] Ready to test 4 extractors
```

## Directory Structure

```plaintext
extractor2/
├── check_extractors.py
├── outstanding_shares_updater.py
├── src/
│   ├── custom_domain_extractors.py
│   └── improved_custom_domain_extractors.py
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Development

- **Run tests**:
  ```bash
  pytest tests/
  ```
- **Add new extractors**:
  1. Implement extractor function in `src/custom_domain_extractors.py`.
  2. Register extractor in the `DOMAIN_EXTRACTORS` dictionary.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add feature: YourFeature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a Pull Request describing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by robust financial data scraping frameworks.
- Thanks to the open-source community for contributions and feedback. 