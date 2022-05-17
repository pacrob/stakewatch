# stakewatch

for watching stake boxes

## To Run

1) Install docker and docker-compose
2) Rename `sample_config.py` to `config.py`
3) In `config.py`, add/remove/rename your `STAKERS` and enter urls for them and your `SOURCE_OF_TRUTH`
4) In `config.py`, adjust the `BLOCK_THRESHOLDS` and `TIME_THRESHOLDS` to your preference
5) The `use_pagerduty` flag in `app.py` determines if alert information is sent to PagerDuty. To enable it, set the flag to `True` and get the PagerDuty Integration Key from your account and enter it in `config.py`.
6) At the command line:

```bash
docker-compose up --build
```
