---
name: seeded-fault-casual-in-feature-columns
description: Seeded fault testing "casual" leakage guard in feature_columns()
metadata:
  type: feedback
---

**Fault:** Added `["casual"]` to the return list of `feature_columns()` function in `src/features.py`, bypassing the `FORBIDDEN` filter.

**Guardrail that caught it:** 
- The hook `.claude/hooks/check_leakage.sh` (PostToolUse) detected and reported failure immediately after the edit
- Test `tests/test_leakage.py::test_no_forbidden_features` failed with: `forbidden columns in feature set: {'casual'}`

**What this teaches:**
1. The leakage test validates that `feature_columns()` correctly filters forbidden columns
2. The hook fires on tool use edits to provide immediate feedback
3. Even if someone tried to "weaken" the guard, the test would catch it by asserting the invariant directly

**Why this matters per CLAUDE.md:** 
> Never put casual or registered in a feature set: `casual + registered == cnt` exactly. `src/config.py` lists these and other excluded columns with the reason for each.
