"""
Data sources for MACRO EDGE AI.
Fetches real market prices via yfinance (no key required).
Economic series via optional FRED API.
Falls back to clearly labeled DEMO mode with historical sample data.
Never fabricates live values as real.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np
import yfinance as yf
from dotenv import load_dotenv

from config import MARKETS, MARKET_NAMES, HIGH_IMPACT_EVENTS, STALE_THRESHOLDS, DEMO_MODE_LABEL

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")

class DataSources:
    def __init__(self):
        self.demo_mode = not bool(FRED_API_KEY)
        self.fred = None
        if FRED_API_KEY:
            try:
                from fredapi import Fred
                self.fred = Fred(api_key=FRED_API_KEY)
            except Exception:
                self.demo_mode = True

    def get_price_data(self, ticker: str, period: str = "5d", interval: str = "1h") -> Tuple[pd.DataFrame, Dict]:
        """Fetch real price data. Returns df and metadata (source, timestamp, is_demo, stale)."""
        meta = {
            "source": "yfinance",
            "fetched_at": datetime.utcnow().isoformat(),
            "is_demo": False,
            "stale": False,
            "warning": None,
        }
        try:
            data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
            if data.empty:
                raise ValueError("Empty data")
            data.index = pd.to_datetime(data.index)
            age_hours = (datetime.utcnow() - data.index[-1].to_pydatetime().replace(tzinfo=None)).total_seconds() / 3600
            if age_hours > STALE_THRESHOLDS["price"]:
                meta["stale"] = True
                meta["warning"] = f"Price data is {age_hours:.1f}h old."
            return data, meta
        except Exception as e:
            meta["is_demo"] = True
            meta["source"] = "demo_fallback"
            meta["warning"] = f"Failed to fetch real prices ({str(e)}). Using DEMO sample."
            dates = pd.date_range(end=datetime.utcnow(), periods=120, freq="h")
            base = 1.08 if "EUR" in ticker else 2000 if "GC" in ticker else 1.25
            prices = base + pd.Series(range(len(dates))) * 0.0001 + np.random.normal(0, 0.001, len(dates))
            df = pd.DataFrame({
                "Open": prices,
                "High": prices + 0.0005,
                "Low": prices - 0.0005,
                "Close": prices,
                "Volume": 1000,
            }, index=dates)
            return df, meta

    def get_economic_series(self, series_id: str, limit: int = 24) -> Tuple[pd.DataFrame, Dict]:
        """Fetch economic series. Real via FRED if key present, else DEMO."""
        meta = {
            "source": "FRED" if self.fred else "demo",
            "fetched_at": datetime.utcnow().isoformat(),
            "is_demo": not bool(self.fred),
            "stale": False,
            "warning": None if self.fred else DEMO_MODE_LABEL,
        }
        if self.fred:
            try:
                data = self.fred.get_series(series_id, observation_start=(datetime.utcnow() - timedelta(days=365*2)).strftime("%Y-%m-%d"))
                df = data.reset_index()
                df.columns = ["date", "value"]
                df["date"] = pd.to_datetime(df["date"])
                df = df.tail(limit)
                if not df.empty:
                    age_days = (datetime.utcnow() - df["date"].iloc[-1].to_pydatetime()).days
                    if age_days > 30:
                        meta["stale"] = True
                        meta["warning"] = f"Series last updated ~{age_days} days ago."
                return df, meta
            except Exception as e:
                meta["is_demo"] = True
                meta["warning"] = f"FRED fetch failed ({str(e)}). Using DEMO."
        
        dates = pd.date_range(end=datetime.utcnow() - timedelta(days=30), periods=limit, freq="MS")
        values = [3.2 + i*0.05 + (0.1 if i % 3 == 0 else 0) for i in range(limit)]
        df = pd.DataFrame({"date": dates, "value": values})
        meta["is_demo"] = True
        meta["source"] = "demo_sample"
        return df, meta

    def get_upcoming_events(self) -> pd.DataFrame:
        """Return structured list of high-impact events. In production, integrate calendar API.
        Currently uses known event types with demo timing."""
        now = datetime.utcnow()
        events = []
        for ev in HIGH_IMPACT_EVENTS:
            next_date = now + timedelta(days=7 + hash(ev["name"]) % 14)
            events.append({
                "event": ev["name"],
                "code": ev["code"],
                "scheduled": next_date.strftime("%Y-%m-%d %H:%M UTC"),
                "impact": ev["impact"],
                "consensus": "N/A (DEMO - fetch from calendar source)",
                "previous": "N/A (DEMO)",
                "is_demo": True,
            })
        return pd.DataFrame(events)

    def get_market_snapshot(self) -> Dict:
        """Current prices for all markets with metadata."""
        snapshot = {}
        for ticker in MARKETS:
            df, meta = self.get_price_data(ticker, period="1d", interval="1m")
            if not df.empty:
                last_close = df["Close"].iloc[-1]
                price_val = float(last_close) if not isinstance(last_close, pd.Series) else float(last_close.iloc[0])
            else:
                price_val = None
            snapshot[MARKET_NAMES.get(ticker, ticker)] = {
                "price": price_val,
                "meta": meta,
            }
        return snapshot
