"""Tests for macro_engine.py"""

import pytest
from macro_engine import MacroEngine
from data_sources import DataSources

@pytest.fixture
def engine():
    return MacroEngine(DataSources())

def test_pre_news_scenarios(engine):
    result = engine.pre_news_scenarios("CPI")
    assert "bullish" in result
    assert "bearish" in result
    assert "neutral" in result
    assert "methodology" in result
    assert "disclaimer" in result

def test_post_news_analysis(engine):
    result = engine.post_news_analysis("NFP", actual=200, consensus=180, previous=175)
    assert result["surprise"] == 20
    assert result["direction_bias"] in ["bullish_usd", "bearish_usd", "neutral"]
    assert "disclaimer" in result

def test_risk_calculator(engine):
    result = engine.risk_calculator(10000, 1.0, 20)
    assert result["risk_amount"] == 100.0
    assert result["suggested_lots"] > 0
    assert "event_warning" in result

def test_simple_model_runs(engine):
    result = engine.simple_surprise_model("CPIAUCSL")
    assert "trend_slope_per_period" in result or "error" in result
    assert "meta" in result or "disclaimer" in result
