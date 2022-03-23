from datetime import datetime, timedelta
from time import time, sleep
from tkinter import W
from helper_functions import (
    get_chain_info,
    send_alerts
)

from sql_alch import (
    connect_to_db,
    write_to_db
)

import sys
sys.path.append("..")
from config import (
    SOURCE_OF_TRUTH,
    STAKERS,
    BLOCK_THRESHOLDS,
)

DELAY_BETWEEN_PROVIDER_CHECKS = 30 

use_pagerduty = False


WARNING, DANGER = BLOCK_THRESHOLDS["warning"], BLOCK_THRESHOLDS["danger"]
truth = {"url": SOURCE_OF_TRUTH, "nickname": "truth"}

stakers = []
for k, v in STAKERS.items():
    staker_data = { "url": v }
    staker_data["nickname"] = k
    stakers.append(staker_data)

# keep track of stakers still within the repeat_alert threshold
recently_alerted = {}

table, connection, metadata = connect_to_db()

def main_event():
    # get info from truth provider
    truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])
    truth["time_stamp"]= datetime.now()
    truth["blocks_out_of_sync"] = 0
    truth["ui_background"] = "bg-primary"

    # get info from stakers
    for staker in stakers:
        staker["connected"], staker["chain_id"], staker["latest_block"] = get_chain_info(staker["url"])
        staker["time_stamp"] = datetime.now()
        try:
            staker["blocks_out_of_sync"] = int(truth["latest_block"]) - int(staker["latest_block"])
        except:
            staker["blocks_out_of_sync"] = 'unknown'
        
        if staker["blocks_out_of_sync"] == 'unknown':
            staker["ui_background"] = "bg-danger"
        elif staker["blocks_out_of_sync"] < WARNING:
            staker["ui_background"] = "bg-primary"
        elif staker["blocks_out_of_sync"] < DANGER:
            staker["ui_background"] = "bg-warning"
        else:
            staker["ui_background"] = "bg-danger"
            

        
    stakers.append(truth)

    # write truth and staker info to db
    write_to_db(table, connection, metadata, stakers)
    
    # TODO determine if stakers are out of sync & send alerts
    
        # if staker["connected"] and truth["connected"]:
        #     block_diff = truth["latest_block"] - staker["latest_block"]
        #     if block_diff > DANGER:
        #         staker["in_sync"] = False
        #     elif block_diff > WARNING:
        #         staker["in_sync"] = False
        #     else:
        #         staker["in_sync"] = True

        # if staker["time_out_of_sync"] > timedelta(minutes=TIME_THRESHOLDS["initial_alert"]):
        #     if staker["nickname"] not in recently_alerted.keys():
        #         alerts_to_send.append((staker["nickname"], staker["time_out_of_sync"]))

    # send alerts
    # if len(alerts_to_send) > 0:
    #     send_alerts(alerts_to_send, recently_alerted, use_pagerduty)


    # clear recently_alerted that are past the repeat threshold
    # now = datetime.now()
    # recently_alerted_to_reset = []
    # for k, v in recently_alerted.items():
    #     if abs(v - now) > timedelta(minutes=TIME_THRESHOLDS["repeat_alert"]):
    #         recently_alerted_to_reset.append(k)
    #         print(f'adding {k} to be deleted from recently alerted')

    # for staker in recently_alerted_to_reset:
    #     del recently_alerted[staker]
    #     print(f'deleting {k} from recently alerted')
        
    print(f'{stakers=}', flush=True)
    # print(f'{recently_alerted=}')

starttime = time()
while True:
    print("tick")
    main_event()
    sleep(DELAY_BETWEEN_PROVIDER_CHECKS - ((time() - starttime) % DELAY_BETWEEN_PROVIDER_CHECKS))
