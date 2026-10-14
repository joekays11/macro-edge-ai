"""
Configuration for MACRO EDGE AI
Central settings for markets, event types, thresholds, and demo behavior.
"""

from typing import Dict, List

# Markets to track
MARKETS: List[str] = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "USDCHF=X",
    "USDCAD=X",
    "AUDUSD=X",
    "NZDUSD=X",
    "GC=F",  # Gold futures proxy for XAUUSD
]

MARKET_NAMES: Dict[str, str] = {
    "EURUSD=X": "EURUSD",
    "GBPUSD=X": "GBPUSD",
    "USDJPY=X": "USDJPY",
    "USDCHF=X": "USDCHF",
    "USDCAD=X": "USDCAD",
    "AUDUSD=X": "AUDUSD",
    "NZDUSD=X": "NZDUSD",
    "GC=F": "XAUUSD",
}

# High-impact economic events (US-focused for simplicity; extendable)
HIGH_IMPACT_EVENTS: List[Dict] = [
    {"name": "CPI", "code": "CPIAUCSL", "impact": "high", "typical_surprise_threshold": 0.1},
    {"name": "Core CPI", "code": "CPILFESL", "impact": "high", "typical_surprise_threshold": 0.1},
    {"name": "NFP", "code": "PAYEMS", "impact": "high", "typical_surprise_threshold": 50},
    {"name": "GDP", "code": "GDP", "impact": "high", "typical_surprise_threshold": 0.2},
    {"name": "PCE", "code": "PCEPI", "impact": "high", "typical_surprise_threshold": 0.1},
    {"name": "FOMC Rate Decision", "code": "FEDFUNDS", "impact": "high", "typical_surprise_threshold": 0.25},
    {"name": "Unemployment Rate", "code": "UNRATE", "impact": "high", "typical_surprise_threshold": 0.1},
]

# Dashboard theme colors (black/navy with green/gold)
COLORS = {
    "bg": "#0A0E17",
    "card": "#111827",
    "green": "#00C853",
    "gold": "#FFD700",
    "red": "#FF5252",
    "text": "#E5E7EB",
    "muted": "#9CA3AF",
}

# Risk and forecast parameters
RISK_PARAMS = {
    "default_account_size": 10000,
    "max_risk_per_trade_pct": 1.0,
    "event_volatility_multiplier": 1.5,
}

# Data freshness thresholds (hours)
STALE_THRESHOLDS = {
    "price": 1,
    "economic": 24,
}

DEMO_MODE_LABEL = "⚠️ DEMO MODE - Using historical/sample data. Configure API keys in .env for live sources."
