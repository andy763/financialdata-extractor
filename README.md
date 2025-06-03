````markdown
# Stock Price & Outstanding Shares Updater

A one-stop toolkit for automatically:

1. Scraping the latest *outstanding share* counts for a list of ETPs/ETFs.  
2. Pulling up-to-date *stock/price* information.  
3. Writing everything to **`data/Custodians_Results.xlsx`** in a clean, ready-to-use format.

The project is built in Python, uses **Selenium** + **BeautifulSoup** for web scraping, and **openpyxl** for Excel automation. A convenience batch file lets Windows users run both updaters in a single click.

---

## Table of Contents

- [Quick Start (TL;DR)](#quick-start-tldr)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Create and activate a virtual-env *(recommended)*](#2-create-and-activate-a-virtual-env-recommended)
  - [3. Install Python dependencies](#3-install-python-dependencies)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
  - [A. Run **both** updaters in one go (Windows batch file)](#a-run-both-updaters-in-one-go-windows-batch-file)
  - [B. Run **outstanding_shares_updater.py**](#b-run-outstanding_shares_updaterpy)
  - [C. Run **excel_stock_updater.py**](#c-run-excel_stock_updaterpy)
- [Project Structure](#project-structure)
- [Output Files](#output-files)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)
- [Changelog](#changelog)

---

## Quick Start (TL;DR)

```bash
# 1. One-time set-up
git clone https://github.com/<your-username>/stock-updater.git
cd stock-updater
python -m venv .venv           # optional but recommended
source .venv/bin/activate      # Windows → .venv\Scripts\activate
pip install -r requirements.txt

# 2. All-in-one run (Windows):
.\batch_files\run_updater_with_shares.bat

#    …or individual scripts on any OS:
python outstanding_shares_updater.py
python excel_stock_updater.py
````

---

## Prerequisites

| Tool / Library               | Why you need it                                    | Install guide                                                          |
| ---------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| **Git**                      | To clone the repository and keep it up to date.    | [https://git-scm.com/downloads](https://git-scm.com/downloads)         |
| **Python 3.10+**             | Core runtime. Tested on 3.10 & 3.11.               | [https://www.python.org/downloads/](https://www.python.org/downloads/) |
| **pip**                      | Python package manager (bundled with Python ≥3.4). | `python -m ensurepip --upgrade`                                        |
| **Google Chrome / Chromium** | Selenium drives Chrome in the background.          | [https://google.com/chrome](https://google.com/chrome)                 |
| **(Optional) VS Code**       | A friendly code editor/terminal combo.             | [https://code.visualstudio.com/](https://code.visualstudio.com/)       |

> **Why no separate “ChromeDriver” step?**
> The project uses `webdriver-manager`, which downloads and keeps the correct driver version for you automatically.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/stock-updater.git
cd stock-updater
```

> No Git? Click **“Code → Download ZIP”** on GitHub, extract it, and open a terminal in that folder.

### 2. Create and activate a virtual-env *(recommended)*

```bash
python -m venv .venv

# ── Windows
.venv\Scripts\activate

# ── macOS / Linux
source .venv/bin/activate
```

A virtual environment keeps project libraries isolated from system Python.

### 3. Install Python dependencies

```bash
pip install --upgrade pip             # always a good first step
pip install -r requirements.txt
```

`requirements.txt` pins all libraries (Selenium, BeautifulSoup, openpyxl, pandas, etc.) to known-working versions.

---

## Configuration

Out of the box **no extra configuration** is required.
The scripts expect:

```
project_root/
├─ data/
│  └─ Custodians.xlsx            # ⇦ input workbook (ships with the repo)
└─ …
```

* **Input file**: `data/Custodians.xlsx`
  Holds the list of custodians / tickers to scrape.
* **Output file**: `data/Custodians_Results.xlsx`
  Created (or overwritten) by the updaters.

If you keep the default names and folder layout, you can run the scripts as-is. Custom paths can be hard-wired in the code if desired.

---

## How to Run

### A. Run **both** updaters in one go (Windows batch file)

```powershell
.\batch_files\run_updater_with_shares.bat
```

The batch file:

1. Shows a friendly banner.
2. Executes `excel_stock_updater.py`.
3. Executes `outstanding_shares_updater.py`.
4. Pauses so you can read any messages.

### B. Run `outstanding_shares_updater.py`

```bash
python outstanding_shares_updater.py
```

What it does:

1. Opens each custodian’s website, SIX-Group page, or custom extractor.
2. Retrieves the **current outstanding share count**.
3. Writes results (plus helpful logs) to `Custodians_Results.xlsx`.

### C. Run `excel_stock_updater.py`

```bash
python excel_stock_updater.py
```

What it does:

1. Fetches the latest **price, NAV, NAV % change**, etc. for every ticker in `Custodians.xlsx`.
2. Colours cells and adds formatting for easy reading.
3. Saves everything to the same `Custodians_Results.xlsx`.

> You can run the two scripts in either order. They both read from / write to the same workbook without conflict.

---

## Project Structure

```
stock-updater/
│
├─ outstanding_shares_updater.py      # ← shares scraper
├─ excel_stock_updater.py             # ← price & NAV updater
│
├─ batch_files/                       # convenience .bat launchers
│   ├─ run_updater_with_shares.bat
│   └─ … (other helpers & tests)
│
├─ data/
│   ├─ Custodians.xlsx                # input list of tickers
│   └─ Custodians_Results.xlsx        # output workbook (created)
│
├─ src/                               # reusable scraper components
│   ├─ custom_domain_extractors.py
│   ├─ improved_custom_domain_extractors.py
│   └─ sixgroup_shares_extractor.py
│
├─ backups/                           # timestamped backups of scripts
├─ requirements.txt
└─ README.md
```

---

## Output Files

| File                               | Description                                                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `data/Custodians_Results.xlsx`     | The master workbook generated by the scripts. Each run overwrites the file (a timestamped backup is made automatically). |
| `data/Custodians_<timestamp>.xlsx` | Fallback copy if the primary results file is locked or missing.                                                          |
| `logs/<date>.log` *(if enabled)*   | Detailed scraping/debug logs (level controlled in each script).                                                          |

---

## Troubleshooting & FAQ

<details>
<summary><strong>Chrome closes instantly / “chrome not reachable”</strong></summary>

* Make sure Google Chrome is installed and not running in the background.
* Update Chrome (Menu → Help → About Google Chrome). `webdriver-manager` always fetches the matching driver, but only if Chrome itself is up to date.

</details>

<details>
<summary><strong>“ElementNotVisible” or time-outs</strong></summary>

Websites occasionally change layouts or add cookie banners.
Try rerunning—many extractors include fallbacks. If it keeps failing, open an issue with the URL in question.

</details>

<details>
<summary><strong>Excel says the file is locked</strong></summary>

* Close any open Excel window using `Custodians_Results.xlsx`.
* Re-run the script; it will create a timestamped copy if needed.

</details>

<details>
<summary><strong>Can I use Firefox / Edge instead of Chrome?</strong></summary>

Yes. Replace the Chrome driver set-up in each script with the equivalent *GeckoDriver* (Firefox) or *EdgeDriver* code. Remember to install the appropriate driver binaries or adjust `webdriver-manager` calls.

</details>

---

## Contributing

1. Fork the repo and create a feature branch.
2. Run `pre-commit install` (optional hooks).
3. Submit a pull request—please describe **what** and **why**.

Bug reports are welcome via GitHub Issues.

---

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## Credits

* **Selenium 4** – browser automation
* **BeautifulSoup 4** – HTML parsing
* **openpyxl** – Excel read/write
* **webdriver-manager** – automatic driver downloads
* **pandas / dateutil / tqdm / colorama** – data wrangling & CLI niceties
* …and the awesome open-source community.

---

## Changelog

| Date (YYYY-MM-DD) | Version | Notes                 |
| ----------------- | ------- | --------------------- |
| 2025-06-03        | 1.0.0   | First public release. |

```

---