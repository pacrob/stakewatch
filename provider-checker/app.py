from dataclasses import dataclass
from datetime import datetime, timedelta
from time import time, sleep
from tkinter import W
from helper_functions import (
    get_chain_info,
    get_formatted_datetime,
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

# keep track of stakers still within the repeat_alert threshold
recently_alerted = {}

table, connection, metadata = connect_to_db()

def main_event():
    stakers = []
    for k, v in STAKERS.items():
        staker_data = { "url": v }
        staker_data["nickname"] = k
        stakers.append(staker_data)
    # get info from truth provider
    truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])
    truth["time_stamp"] = get_formatted_datetime()
    truth["blocks_out_of_sync"] = 0
    truth["ui_background"] = "bg-primary"

    # get info from stakers
    for staker in stakers:
        staker["connected"], staker["chain_id"], staker["latest_block"] = get_chain_info(staker["url"])
        staker["time_stamp"] = get_formatted_datetime()
        if staker["connected"]:
            staker["blocks_out_of_sync"] = int(truth["latest_block"]) - int(staker["latest_block"])
            if staker["blocks_out_of_sync"] < WARNING:
                staker["ui_background"] = "bg-primary"
            elif staker["blocks_out_of_sync"] < DANGER:
                staker["ui_background"] = "bg-warning"
            else:
                staker["ui_background"] = "bg-danger"
            
        else:
            staker["blocks_out_of_sync"] = 'unknown'
            staker["ui_background"] = "bg-danger"

        
    stakers.append(truth)

    # write truth and staker info to db
    # print(stakers, flush=True)
    str_stakers = str(stakers)
    dict_stakers = [{'providers_blob': str_stakers}]
    # print(type(str_stakers), flush=True)
    write_to_db(table, connection, metadata, dict_stakers)

    
    # TODO determine if stakers are out of sync & send alerts
    # for x in stakers[0]: print(x, flush=True) 
    # print(f'{stakers=}', flush=True)

starttime = time()
while True:
    print("tick", flush=True)
    main_event()
    sleep(DELAY_BETWEEN_PROVIDER_CHECKS - ((time() - starttime) % DELAY_BETWEEN_PROVIDER_CHECKS))
