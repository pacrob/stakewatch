from web3 import Web3
from flask import Flask, render_template, json

app = Flask(__name__)

with open("config.json", "r") as config:
    data = json.load(config)

def get_chain_info(url: str):
    w3 = Web3(Web3.HTTPProvider(url))
    connected = w3.isConnected()
    chain_id = "unknown"
    latest_block = "unknown"
    
    if connected:
        chain_id = w3.eth.chain_id
        latest_block = w3.eth.block_number

    return connected, chain_id, latest_block

@app.route("/")
def index():

    truth = data["source_of_truth"]
    truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])

    stakers = []
    for staker in data["stakers"]:
        staker_data = data["stakers"][staker]
        staker_data["nickname"] = staker
        stakers.append(staker_data)

    for staker in stakers:
        staker["connected"], staker["chain_id"], staker["latest_block"] = get_chain_info(staker["url"])

    print(stakers)

    return render_template(
        "index.html",
        source_of_truth = truth,
        stakers = stakers
    )