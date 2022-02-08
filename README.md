# stakewatch
webapp for watching stake boxes

## To Run
1) Set up your virtualenv with from requirements.txt
2) Rename `sample_config.py` to `config.py`
3) In `config.py`, enter the urls for your source of truth and the boxes you want to watch
4) In `config.py`, adjust the `BLOCK_THRESHOLDS` and `TIME_THRESHOLDS` to your preference
5) At the command line:
```
$ export FLASK_ENV=development
$ flask run
```