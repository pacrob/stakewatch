BLOCK_THRESHOLDS = {
    "warning": 5,  # UI turns yellow if more than this many blocks out of sync
    "danger": 25,  # UI turns red if more than this many blocks out of sync
}
PAGERDUTY_ALERT_URL = "https://events.pagerduty.com/v2/enqueue"
PAGERDUTY_INTEGRATION_KEY = "key_goes_here"
SECONDS_BETWEEN_PROVIDER_CHECKS = 30
SOURCE_OF_TRUTH = "url_goes_here"
STAKERS = { 
    "staker1": "url_goes_here",
    "staker2": "url_goes_here",
    "staker3": "url_goes_here",
}
TIME_THRESHOLD = 5  # send an alert every this many minutes
