from web3 import Web3
from flask import Flask, render_template, json
from datetime import datetime

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

with open("config.json", "r") as config:
    data = json.load(config)

@app.route("/")
def index():

    warning, danger = data["block_thresholds"]["warning"], data["block_thresholds"]["danger"]

    truth = data["source_of_truth"]
    truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])

    stakers = []
    for staker in data["stakers"]:
        staker_data = data["stakers"][staker]
        staker_data["nickname"] = staker
        stakers.append(staker_data)

    for staker in stakers:
        staker["connected"], staker["chain_id"], staker["latest_block"] = get_chain_info(staker["url"])
        
        block_diff = truth["latest_block"] - staker["latest_block"]
        if block_diff > danger:
            staker["background"] = "bg-danger"
        elif block_diff > warning:
            staker["background"] = "bg-warning"
        else:
            staker["background"] = "bg-success"


    print(f"{stakers=}")

    now = datetime.now()
    print(f"{now=}")

    return render_template(
        "index.html",
        source_of_truth = truth,
        stakers = stakers,
        time = now,
    )