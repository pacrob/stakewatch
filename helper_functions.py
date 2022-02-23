import json
import requests
from datetime import datetime
from web3 import Web3

from config import (
    PAGERDUTY_ALERT_URL,
    PAGERDUTY_INTEGRATION_KEY,
)

def get_chain_info(url: str):
    w3 = Web3(Web3.HTTPProvider(url))
    try:
        connected = w3.isConnected()
    except:
        connected = False

    chain_id = "unknown"
    latest_block = "unknown"
    
    if connected:
        chain_id = w3.eth.chain_id
        latest_block = w3.eth.block_number

    return connected, chain_id, latest_block

def send_alerts(stakers: list[tuple], recently_alerted: dict, use_pagerduty: bool):
    if use_pagerduty:
        alert = {
            "payload": {
                "summary": "stakers out of sync",
                "source": "stakewatch",
                "severity": "error",
            },
            "routing_key": PAGERDUTY_INTEGRATION_KEY,
            "event_action": "trigger",
        }

        alert_json = json.dumps(alert, indent=2)
        r = requests.post(PAGERDUTY_ALERT_URL, data=alert_json)
    # print(f'{r=}')
    for staker in stakers:
        print(f'alerting {staker[0]} out of sync for {staker[1]}')
        recently_alerted[staker[0]] = datetime.now()
        print(f'adding {staker[0]} to recently_alerted')