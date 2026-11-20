---
name: seed-fault
description: Seed an intentional fault in code or test data, run verification checks and hooks to observe what is caught or missed, and revert the fault cleanly. Use whenever someone asks to seed a fault, test a guardrail, or evaluate hook/test coverage on a failure mode.
allowed-tools: Read, Edit, Bash(python -m pytest*), Bash(make*), Bash(git status), Bash(git diff:*)
---

# Current feature set

!`python -c "import pandas as pd; from src.features import feature_columns; print(', '.join(feature_columns(pd.read_parquet('data/processed/features.parquet'))))"`

# Seeding a fault: $ARGUMENTS

Work in this order. Do not skip step 2 or step 5.

1. **State the fault and target safeguard in one sentence.** Name the seeded fault (`$ARGUMENTS`) and which file/guard it targets. Optionally, add (`PostToolUse` hook, `tests/test_leakage.py`, `make test`, or permissions) you expect to react—or miss it.

2. **Capture baseline state before editing.** Run `git status` and `make test` so you have a clean baseline and can verify whether any failure after seeding is caused by the injected fault. Tell the user explicitly this was run.

3. **Inject the fault cleanly.** Make the minimal targeted edit described in `$ARGUMENTS` using `Edit` (for example, removing a line of code, weakening a guard, shifting a lag/window, or altering a test fixture). Keep the change isolated to the named target file(s) so it can be reverted without collateral damage. Explicitly show the user what lines were edited/added/removed.

4. **Observe hooks, test output, and blind spots.** Run `make test` (and check any hook `stderr` or permission behavior). Explicitly tell the user factually:
   - Whether `PostToolUse` fired or stayed silent (and why). If it fired, give the verbatim error with a summary of what it means.
   - Tell verbatim tests passed or failed, and whether a blind spot or permission block occurred. 
   - What safeguard *would* catch the fault if current checks missed it.

5. **Revert the fault and confirm clean state.** Revert the seeded change back to the baseline state, then run `git status --short` and `make test` to confirm the working tree is clean and all tests pass again. Do not permanently log anything down, make sure it is all said in the output.

Do not leave seeded faults in the working tree or report unverified passes as clean runs. If a tool call is denied by permissions, report the exact denial and check disk/git state rather than assuming the action succeeded.
