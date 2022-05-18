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
    TIME_THRESHOLD,
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

def send_alerts(out_of_sync_stakers: list[tuple], recently_alerted: dict, use_pagerduty: bool):
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
    print('send_alerts called', flush=True) 
    print(f'{out_of_sync_stakers=}', flush=True)
    print(f'{recently_alerted=}', flush=True)

    for staker in out_of_sync_stakers:
        if staker["nickname"] not in recently_alerted.keys():
            print(f'alerting {staker["nickname"]} out of sync for {staker["time_out_of_sync"]}', flush=True)
            recently_alerted[staker["nickname"]] = datetime.now()
            print(f'adding {staker["nickname"]} to recently_alerted', flush=True)

        else:
            if datetime.now() - recently_alerted[staker["nickname"]] > timedelta(minutes=TIME_THRESHOLD):
                del recently_alerted[staker["nickname"]]
                print(f'removing {staker["nickname"]} from recently_alerted', flush=True)
        
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