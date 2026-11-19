## Seeded Fault #1, Forbidden Column in feature_columns (src/features.py)
In order to fire off the hook's stderr, the edit that causes the error is done through a Claude prompt, specifically *"In src/features.py, edit feature_columns so that it returns the list of feature columns plus "casual". Do not run tests or fix it yet."* 

This modified `feature_columns()` to store the original list it returned, `[c for c in numeric if c not in FORBIDDEN]` in a variable called filtered. Then, the function now ends with `return ["casual"] + filtered`. Previously, the last line in `feature_columns()` was `return [c for c in numeric if c not in FORBIDDEN]` which has now been replaced by 2 lines: 

`filtered = [c for c in numeric if c not in FORBIDDEN]` and `return ["casual"] + filtered`

### The PostToolUse hook sent the stderr:

PostToolUse:Edit hook reported a problem
[${CLAUDE_PROJECT_DIR}/.claude/hooks/check_leakage.sh]: Leakage tests failed after editing C:\Users\night\Downloads\bikeshare-open\src\features.py:

feats =         dteday  instant  season      yr mnth  ... month_cos weather_severity  cnt_lag_1  cnt_lag_7   cnt_roll_7
0   20... 731.0  WINTER  2012.0  DEC  ...  1.000000              1.0     1796.0      920.0  1531.428571

[714 rows x 28 columns]

    def test_no_forbidden_features(feats):
        """Guards the gate, not the data: feature_columns() excludes FORBIDDEN by
        construction, so this cannot discover a *new* leaky column. What it
        catches is someone editing feature_columns() or FORBIDDEN -- which is
        exactly the fault the Step 7 hook demonstrates."""
        cols = set(feature_columns(feats))
>       assert not (cols & FORBIDDEN), f"forbidden columns in feature set: {cols & FORBIDDEN}"
E       AssertionError: forbidden columns in feature set: {'casual'}
E       assert not ({'atemp', 'casual', 'cnt_lag_1', 'cnt_lag_7', 'cnt_roll_7', 'dayofweek', ...} & {'casual', 'cnt', 'cnt_2d_bfr', 'days_since_2011', 'instant', 'registered', ...})

tests\test_leakage.py:31: AssertionError
=============================================== short test summary info ===============================================
FAILED tests/test_leakage.py::test_no_forbidden_features - AssertionError: forbidden columns in feature set: {'casual'}
1 failed, 6 passed in 0.65s


