import json
import requests
from datetime import datetime, timedelta
from web3 import Web3

import sys
sys.path.append("..")
from config import (
    BLOCK_THRESHOLDS,
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

    connected = 1 if connected else 0
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
        
def format_datetime(dt_object):
    if type(dt_object) == datetime:
        return str(dt_object.replace(microsecond=0))
    elif type(dt_object) == timedelta:
        return str(dt_object)
    
def set_ui_background(blocks_out_of_sync):
    if blocks_out_of_sync < BLOCK_THRESHOLDS["warning"]:
        return "bg-primary"
    elif blocks_out_of_sync < BLOCK_THRESHOLDS["danger"]:
        return "bg-warning"
    else:
        return "bg-danger"