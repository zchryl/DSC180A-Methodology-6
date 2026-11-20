# Decisions

One line per methodological decision: what you chose, why, and what it changed.
Agents append here via the `/new-feature` skill; you append here by hand.

- Exclude `casual`, `registered`: they sum to `cnt` exactly. Leaky model R^2 1.000 -> honest ridge 0.583.
- Exclude `cnt_2d_bfr`: a shipped 2-day lag we cannot test the alignment of. Build our own lags instead.
- Exclude `instant`, `yr`, `days_since_2011`: time indexes let a tree predict a flat constant past 2011 and a linear model extrapolate a trend we have no grounds for.
- Split 2011 / H1 2012 / H2 2012 by date. Test set touched once, after all feature work.
- Report mean and persistence baselines with every score. Persistence (test R^2 0.510, MAE 840) is within 0.07 R^2 of ridge and beats it on MAE; that caveat goes in the report.

**/new-feature: tempest (avg of temp+atemp)**
- What: `tempest = (temp + atemp) / 2`, a same-day temperature average.
- Availability argument: At prediction time for date *d*, `temp` and `atemp` are measured on day *d*; no future data needed.
- Validation delta: ridge R² moved from 0.6475 (baseline) to 0.6476 (+0.0001), well below the 0.01 noise threshold; drop per policy.
Dropped tempest feature: +0.0001 R² improvement fell below 0.01 noise threshold.


Noted 11/18
## Step 2 Analysis
1. The model correctly identified that there are 728 rows with a date range of 2011-01-03 to 2012-12-31
.
2. The model correctly identified that the weather column exists with 3 values, GOOD, MISTY, and BAD, but DID NOT note the value counts of these labels in the categorical column
3. The model identified that the day 2011-03-10 is missing because the humidity = 0. However, the model also mentioned 2011-01-01 and 2011-01-02 as missing because "data starts 2011-01-03." This may be a sign of the model finding "more" detail, connecting these two dates to missing data to mean a missing calendar day.
4. Model correctly identified "casual" and "registered" as leakage columns, as well as rationalizing th at these two columns would lead to the model learning to add, instead of a pattern.  -->

Noted 11/19 12:50pm
New feature "tempest". Availability argument: At prediction time for date d, tempest (average of temp and atemp) is known on day d because temperature is measured on day d. Validation delta +0.00001, dropped

Noted 11/19 10:20pm
Created skill /seed-fault. Directions **explicitly** list the outputs and *hook stderr* if any arose to replicate Exercise 2 findings. Also show code changes, run make test before/after to verify code untouched

Noted 11/19 10:25pm
/seed-fault creates its own "memory/" folder. This will be allowed, since it does not interfere with other folders and serves as a log for the usage of the skill. 

Noted 11/19 10:26pm
Executions of seed faults in Exercise 2, `cp` and remove `raise` did not fire stderr from hook. Assuming this is intentional because PostToolUse does not check for these changes, `cp` automatically denied


