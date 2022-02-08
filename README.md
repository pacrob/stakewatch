# stakewatch
webapp for watching stake boxes

## To Run
1) Set up your virtualenv with from requirements.txt
2) Rename `sample_config.py` to `config.py`
3) In `config.py`, add/remove/rename your `STAKERS` and enter urls for them and your `SOURCE_OF_TRUTH`
4) In `config.py`, adjust the `BLOCK_THRESHOLDS` and `TIME_THRESHOLDS` to your preference
5) The webpage will automatically refresh every 30 seconds
    - this can be changed by editing the `content` value of the following line in templates/layout.html:
    - `<meta http-equiv="refresh" content="30">`
6) At the command line:
```
$ export FLASK_ENV=development
$ flask run
```