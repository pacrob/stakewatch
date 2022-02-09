BLOCK_THRESHOLDS = {
    "warning": 5,  # UI turns yellow if more than this many blocks out of sync
    "danger": 25,  # UI turns red if more than this many blocks out of sync
}
PAGERDUTY_ALERT_URL = "https://events.pagerduty.com/v2/enqueue"
PAGERDUTY_INTEGRATION_KEY = "key_goes_here"
SOURCE_OF_TRUTH = "url_goes_here"
STAKERS = { 
    "staker1": "url_goes_here",
    "staker2": "url_goes_here",
    "staker3": "url_goes_here",
}
TIME_THRESHOLDS = {
    "initial_alert": 1, # first alert sent after this many minutes out of sync
    "repeat_alert": 5, # repeat alerts sent every this many minutes while still out of sync
}
