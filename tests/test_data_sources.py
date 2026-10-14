"""Tests for data_sources.py"""

import pytest
from data_sources import DataSources

@pytest.fixture
def ds():
    return DataSources()

def test_get_price_data_returns_df_and_meta(ds):
    df, meta = ds.get_price_data("EURUSD=X", period="1d", interval="1h")
    assert not df.empty or meta["is_demo"]
    assert "source" in meta
    assert "fetched_at" in meta
    assert "is_demo" in meta

def test_get_economic_series(ds):
    df, meta = ds.get_economic_series("CPIAUCSL")
    assert "date" in df.columns
    assert "value" in df.columns
    assert "is_demo" in meta
    assert meta["is_demo"] or "FRED" in meta["source"]

def test_get_upcoming_events(ds):
    events = ds.get_upcoming_events()
    assert not events.empty
    assert "event" in events.columns
    assert "is_demo" in events.columns

def test_market_snapshot(ds):
    snap = ds.get_market_snapshot()
    assert len(snap) > 0
    for name, info in snap.items():
        assert "price" in info
        assert "meta" in info
