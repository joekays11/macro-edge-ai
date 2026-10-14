"""
Macro forecasting engine for MACRO EDGE AI.
Provides pre-news scenarios, post-news comparison, simple historical surprise analysis,
risk calculations, and transparent methodology notes.
Uses point-in-time logic; no look-ahead bias in historical evaluation.
Does NOT guarantee accuracy or profits. All outputs include uncertainty.
"""

from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from config import RISK_PARAMS, HIGH_IMPACT_EVENTS
from data_sources import DataSources

class MacroEngine:
    def __init__(self, data_sources: Optional[DataSources] = None):
        self.ds = data_sources or DataSources()
        self.history: List[Dict] = []  # In-memory forecast history for demo

    def pre_news_scenarios(self, event_name: str, consensus: Optional[float] = None) -> Dict:
        """Generate bullish/bearish/neutral scenarios for an upcoming event.
        Based on typical historical reactions (simplified, transparent).
        """
        scenarios = {
            "event": event_name,
            "methodology": "Historical average price reaction to positive/negative surprises for similar US data releases. Not a prediction.",
            "uncertainty": "High - markets react to surprise relative to consensus and context (growth, inflation regime).",
            "bullish": {
                "condition": f"Actual > consensus by more than threshold (e.g. stronger data or lower inflation depending on context)",
                "typical_reaction": "USD strength / Gold weakness for inflation beats; mixed for growth",
                "explanation": "Stronger-than-expected data often supports USD via higher rate expectations. Gold may sell off on higher real yields.",
            },
            "bearish": {
                "condition": "Actual < consensus (weaker data or higher inflation)",
                "typical_reaction": "USD weakness / Gold strength",
                "explanation": "Weaker data can lower rate hike odds or increase cut odds, pressuring USD and supporting gold.",
            },
            "neutral": {
                "condition": "In-line with consensus",
                "typical_reaction": "Muted or mean-reversion after initial spike",
                "explanation": "No surprise often leads to limited sustained directional move once positioning adjusts.",
            },
            "is_demo": self.ds.demo_mode,
            "disclaimer": "Educational scenarios only. Not trading advice. Past reactions do not guarantee future results.",
        }
        return scenarios

    def post_news_analysis(self, event_name: str, actual: float, consensus: float, previous: float) -> Dict:
        """Compare actual vs consensus and estimate directional bias."""
        surprise = actual - consensus
        direction = "bullish_usd" if surprise > 0 else "bearish_usd" if surprise < 0 else "neutral"
        magnitude = abs(surprise)
        analysis = {
            "event": event_name,
            "actual": actual,
            "consensus": consensus,
            "previous": previous,
            "surprise": surprise,
            "direction_bias": direction,
            "magnitude": "large" if magnitude > 0.2 else "moderate" if magnitude > 0.05 else "small",
            "note": "Bias is directional only based on surprise sign. Context (Fed path, positioning) dominates.",
            "is_demo": True if consensus is None else self.ds.demo_mode,
            "disclaimer": "Post-event analysis for education. Not a signal.",
        }
        self.history.append({
            "timestamp": pd.Timestamp.utcnow().isoformat(),
            "type": "post_news",
            "event": event_name,
            "surprise": surprise,
        })
        return analysis

    def simple_surprise_model(self, series_id: str) -> Dict:
        """Fit a simple linear model on historical values to illustrate trend.
        For transparency; not for live forecasting.
        """
        df, meta = self.ds.get_economic_series(series_id)
        if len(df) < 5:
            return {"error": "Insufficient data", "meta": meta}
        X = np.arange(len(df)).reshape(-1, 1)
        y = df["value"].values
        model = LinearRegression().fit(X, y)
        trend_slope = float(model.coef_[0])
        return {
            "series": series_id,
            "trend_slope_per_period": trend_slope,
            "interpretation": "Positive slope = rising trend in historical sample.",
            "r2": float(model.score(X, y)),
            "meta": meta,
            "methodology": "Ordinary least squares on available observations. Point-in-time: uses only past data.",
            "disclaimer": "Trend description only. No predictive claim.",
        }

    def risk_calculator(self, account_size: float, risk_pct: float, stop_pips: float, pair: str = "EURUSD") -> Dict:
        """Basic position size calculator with event risk warning."""
        risk_amount = account_size * (risk_pct / 100)
        pip_value_per_lot = 10
        lots = risk_amount / (stop_pips * pip_value_per_lot) if stop_pips > 0 else 0
        warning = "Event risk elevated: volatility often 1.5-3x normal around high-impact releases. Reduce size."
        return {
            "account_size": account_size,
            "risk_pct": risk_pct,
            "risk_amount": round(risk_amount, 2),
            "stop_pips": stop_pips,
            "suggested_lots": round(lots, 2),
            "event_warning": warning,
            "disclaimer": "Calculator is approximate. Verify pip values and use proper risk management. Not advice.",
        }

    def get_forecast_history(self) -> pd.DataFrame:
        """Return recorded analysis history (demo persistence)."""
        if not self.history:
            return pd.DataFrame(columns=["timestamp", "type", "event", "surprise"])
        return pd.DataFrame(self.history)

    def performance_note(self) -> str:
        """Transparent note on evaluation limitations."""
        return (
            "Forecast history is session-only in this demo. "
            "True performance evaluation requires stored point-in-time forecasts vs subsequent price moves "
            "with proper walk-forward testing. No accuracy statistics are claimed or fabricated."
        )
