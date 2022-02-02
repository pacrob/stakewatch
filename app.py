from web3 import Web3
from flask import Flask, render_template, json
from datetime import datetime

from config import (
    SOURCE_OF_TRUTH,
    STAKERS,
    BLOCK_THRESHOLDS,
    PAGERDUTY_ALERT_URL,
    PAGERDUTY_CHANGE_URL,
    PAGERDUTY_INTEGRATION_KEY
)

app = Flask(__name__)

def get_chain_info(url: str):
    w3 = Web3(Web3.HTTPProvider(url))
    connected = w3.isConnected()
    chain_id = "unknown"
    latest_block = "unknown"
    
    if connected:
        chain_id = w3.eth.chain_id
        latest_block = w3.eth.block_number

    return connected, chain_id, latest_block

WARNING, DANGER = BLOCK_THRESHOLDS["warning"], BLOCK_THRESHOLDS["danger"]
START_TIME = datetime.now()
truth = {"url": SOURCE_OF_TRUTH}

stakers = []
for k, v in STAKERS.items():
    staker_data = { "url": v }
    staker_data["nickname"] = k
    staker_data["last_time_in_sync"] = START_TIME
    staker_data["in_sync"] = True
    staker_data["time_out_of_sync"] = START_TIME - START_TIME
    stakers.append(staker_data)



@app.route("/")
def index():

    truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])
    current_time = datetime.now()

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

    print(f"{stakers=}")
    now = datetime.now()
    print(f"{now=}")

    return render_template(
        "index.html",
        source_of_truth = truth,
        stakers = stakers,
        time = now,
    )