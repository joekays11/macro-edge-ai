# MACRO EDGE AI

Professional Streamlit dashboard for fundamental forex and gold forecasting before economic news releases.

**Markets:** EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, XAUUSD

**Features:**
- Black/navy dashboard with green & gold accents
- Economic calendar structure for high-impact releases (CPI, NFP, FOMC, etc.)
- Pre-news bullish/bearish/neutral scenarios with explanations
- Post-news actual vs consensus analysis
- Real price data via yfinance (falls back to clearly labeled DEMO)
- Optional FRED API for economic series
- Data timestamps, stale-data warnings, missing-data handling
- Transparent methodology & uncertainty indicators
- Forecast history (session) and performance notes
- Risk calculator with event-risk warnings
- Demo mode clearly labeled when API keys missing

**Important:** Educational tool only. Does **not** guarantee predictions, accuracy, or profits. Never fabricates live data as real.

## Quick Start (Windows & macOS)

### Prerequisites
- Python 3.9+ installed ([python.org](https://www.python.org/downloads/))
- Git (optional, for GitHub)

### 1. Clone or download the project
```bash
git clone https://github.com/joekays11/macro-edge-ai.git
cd macro-edge-ai
```

### 2. Create virtual environment
**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Optional: Configure API keys
Copy `.env.example` to `.env` and add free FRED key from https://fred.stlouisfed.org/docs/api/api_key.html
Without key: DEMO MODE (clearly labeled).

### 5. Run the app
```bash
streamlit run app.py
```

### 6. Run tests
```bash
pytest tests/ -v
```

## Streamlit Community Cloud
1. Go to https://share.streamlit.io
2. New app → select joekays11/macro-edge-ai
3. Main file path: app.py
4. Deploy

## Data Sources
- Prices: yfinance (real, no key)
- Economic: optional FRED
- All data tagged with source/timestamp/DEMO flag

Educational only. Not trading advice.
