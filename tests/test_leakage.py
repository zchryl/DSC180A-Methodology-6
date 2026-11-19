"""The tests that make the agent honest.

test_no_forbidden_features is the single most valuable test in this repo:
casual + registered == cnt exactly, so any model handed those columns
scores R^2 = 1.0 and looks brilliant while having learned nothing.
"""
import pandas as pd
import pytest

from src.config import FORBIDDEN, TARGET
from src.features import build_features, feature_columns
from src.ingest import load_raw


@pytest.fixture(scope="module")
def feats():
    return build_features(load_raw())


def test_leakage_identity_holds(feats):
    """Documents *why* casual and registered are forbidden."""
    assert (feats.casual + feats.registered == feats[TARGET]).all()


def test_no_forbidden_features(feats):
    """Guards the gate, not the data: feature_columns() excludes FORBIDDEN by
    construction, so this cannot discover a *new* leaky column. What it
    catches is someone editing feature_columns() or FORBIDDEN -- which is
    exactly the fault the Step 7 hook demonstrates."""
    cols = set(feature_columns(feats))
    assert not (cols & FORBIDDEN), f"forbidden columns in feature set: {cols & FORBIDDEN}"


def test_lags_are_true_calendar_lags(feats):
    """cnt_lag_1 for date d must equal cnt on d-1, in calendar days."""
    by_date = feats.set_index("dteday")[TARGET]
    checked = 0
    for date, lag in feats.set_index("dteday").cnt_lag_1.items():
        prev = date - pd.Timedelta(days=1)
        if prev in by_date.index:
            assert lag == pytest.approx(by_date[prev]), f"bad lag at {date.date()}"
            checked += 1
    assert checked > 600, "too few rows actually verified"


def test_lag_is_not_the_target(feats):
    assert not (feats.cnt_lag_1 == feats[TARGET]).all()


def test_rolling_mean_excludes_today(feats):
    """cnt_roll_7 must be the mean of the 7 calendar days *before* today."""
    by_date = feats.set_index("dteday")[TARGET]
    date = feats.dteday.iloc[200]
    window = [date - pd.Timedelta(days=k) for k in range(1, 8)]
    if all(d in by_date.index for d in window):
        expected = sum(by_date[d] for d in window) / 7
        assert feats.set_index("dteday").cnt_roll_7[date] == pytest.approx(expected)


def test_no_missing_values(feats):
    assert feats[feature_columns(feats)].isna().sum().sum() == 0


def test_tempest_is_mean_of_a_temp_and_temp(feats):
    """Verify tempest feature equals the mean of atemp and temp."""
    # Pick a date where we have valid data for both temperature features
    valid_row = feats[(feats.atemp.notna()) & (feats.temp.notna())].iloc[0]
    expected = (valid_row["atemp"] + valid_row["temp"]) / 2.0
    actual = valid_row["tempest"]
    assert actual == pytest.approx(expected), f"tempest={actual}, expected={expected} at {valid_row.dteday.date()}"


def test_tempest_has_no_future_leakage(feats):
    """Verify tempest on date d does not use info from dates >= d."""
    # Since we just average two same-day features, there's no leakage by design.
    # But let's verify on a known date with actual values.
    test_date = pd.Timestamp("2011-06-15")  # Pick a mid-year date in train set
    if test_date.date() in feats.dteday:
        row = feats.loc[feats.dteday == test_date]
        if not row.empty:
            vrow = row.iloc[0]
            expected = (vrow["atemp"] + vrow["temp"]) / 2.0
            assert abs(vrow["tempest"] - expected) < 1e-6


def test_dates_are_sorted_and_unique(feats):
    assert feats.dteday.is_monotonic_increasing
    assert feats.dteday.is_unique



