## Results
Exercise 1 Before/ After Feature
| Model | Split | R2 Before | R2 After | MAE Before | MAE After |
|---|---|---|---|---|---|
| baseline_mean | valid | -0.9318 | -0.9318 | 2002.2 | 2002.2 |
| baseline_mean | test | -2.1441 | -2.1441 | 2847.7 | 2847.7 |
| baseline_persistence | valid | 0.4507 | 0.4507 | 900.6 | 900.6 |
| baseline_persistence | test | 0.5099 | 0.5099 | 840.1 | 840.1 |
| ridge | valid | 0.6475 | 0.6476 | 832.9 | 832.8 |
| ridge | test | 0.5833 | 0.5833 | 947.1 | 947.1 |
| hgb | valid | 0.2185 | 0.2304 | 1296.6 | 1283.9 |
| hgb | test | -0.4975 | -0.5369 | 1972.6 | 2001.2 | 

## Headline Finding 
The proposed feature `tempest = (temp + atem)/2` combines 2 existing columns at the time of prediction into an averaged column. Evident in the above Before & After table of model scores, `tempest` did not add any distinguishing information to the feature set. Unlike the models in Part 1, the models here are cognizant of the leakage columns `casual + registered`. `tempest` added so little information that it did not influence the `baseline_mean` or `baseline_persistence` models' validation and test scores. Those models' respective validation scores before and after `tempest` was added were -0.9318 and 0.4507. The Gradient boosting model subtley changed its metrics from a validation score of 0.22 to 0.23, but this fluctuation is likely a result of the tree design `hgb` has. `hgb` still outperforms `baseline_mean` in testing (-0.5369 versus -2.1441), despite this added randomness. `tempest` changed the `ridge` model the "most," although all that changed was a `0.0001` difference in validation $R^2$ from 0.6475 to 0.6476. Because the difference in validation score was < 0.01, it is policy to **drop** this new feature as its influence falls under the "noise" threshold.