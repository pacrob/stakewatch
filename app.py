from datetime import datetime, timedelta
from flask import Flask, render_template
from helper_functions import (
    get_chain_info,
    send_pagerduty_alert
)

from config import (
    BLOCK_THRESHOLDS,
    SOURCE_OF_TRUTH,
    STAKERS,
    TIME_THRESHOLDS,
)

app = Flask(__name__)

# setup
WARNING, DANGER = BLOCK_THRESHOLDS["warning"], BLOCK_THRESHOLDS["danger"]
START_TIME = datetime.now()
truth = {"url": SOURCE_OF_TRUTH}

stakers = []
for k, v in STAKERS.items():
    staker_data = { "url": v }
    staker_data["nickname"] = k
    staker_data["last_time_in_sync"] = START_TIME
    staker_data["in_sync"] = False
    staker_data["time_out_of_sync"] = timedelta(0)
    stakers.append(staker_data)

# keep track of stakers still within the repeat_alert threshold
recently_alerted = {}

# this route automatically refreshes based on the number of seconds set in layout.html
# specfically the content value in this line: "<meta http-equiv="refresh" content="30">"
@app.route("/")
def index():

    truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])
    current_time = datetime.now()
    alerts_to_send = []

    for staker in stakers:
        staker["connected"], staker["chain_id"], staker["latest_block"] = get_chain_info(staker["url"])
        
        if staker["connected"] and truth["connected"]:
            block_diff = truth["latest_block"] - staker["latest_block"]
            if block_diff > DANGER:
                staker["background"] = "bg-danger"
                staker["in_sync"] = False
                staker["time_out_of_sync"] = current_time - staker["last_time_in_sync"]
            elif block_diff > WARNING:
                staker["background"] = "bg-warning"
                staker["in_sync"] = False
                staker["time_out_of_sync"] = current_time - staker["last_time_in_sync"]
            else:
                staker["background"] = "bg-success"
                staker["last_time_in_sync"] = current_time
                staker["in_sync"] = True

        if staker["time_out_of_sync"] > timedelta(minutes=TIME_THRESHOLDS["initial_alert"]):
            if staker["nickname"] not in recently_alerted.keys():
                alerts_to_send.append((staker["nickname"], staker["time_out_of_sync"]))

    # send alerts
    if len(alerts_to_send) > 0:
        send_pagerduty_alert(alerts_to_send, recently_alerted)

    # clear recently_alerted that are past the repeat threshold
    now = datetime.now()
    recently_alerted_to_reset = []
    for k, v in recently_alerted.items():
        if abs(v - now) > timedelta(minutes=TIME_THRESHOLDS["repeat_alert"]):
            recently_alerted_to_reset.append(k)
            print(f'adding {k} to be deleted from recently alerted')

    for staker in recently_alerted_to_reset:
        del recently_alerted[staker]
        print(f'deleting {k} from recently alerted')


    # print(f"{stakers=}")
    print(f"{now=}")

    return render_template(
        "index.html",
        source_of_truth = truth,
        stakers = stakers,
        time = now,
    )
