# stakewatch
webapp for watching stake boxes

## To Run
1) Set up a new virtualenv with from the requirements.txt, e.g.:
```
$ pip install virtualenv 
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
2) Rename `sample_config.py` to `config.py`
3) In `config.py`, add/remove/rename your `STAKERS` and enter urls for them and your `SOURCE_OF_TRUTH`
4) In `config.py`, adjust the `BLOCK_THRESHOLDS` and `TIME_THRESHOLDS` to your preference
5) The webpage is set to automatically refresh every 30 seconds
    - This can be changed by editing the `content` value of the following line in templates/layout.html:
    - `<meta http-equiv="refresh" content="30">`
6) The `use_pagerduty` flag in `app.py` determines if alert information is sent to PagerDuty. To enable it, set the flag to `True` and get the PagerDuty Integration Key from your account and enter it in `config.py`.
6) At the command line:
```
$ export FLASK_ENV=development
$ flask run
```
