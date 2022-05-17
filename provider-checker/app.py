from datetime import datetime, timedelta
from time import time, sleep
from helper_functions import (
    get_chain_info,
    format_datetime,
    send_alerts,
    set_ui_background,
)

from sql_alch import (
    connect_to_db,
    write_to_db,
)

import sys
sys.path.append("..")
from config import (
    BLOCK_THRESHOLDS,
    SECONDS_BETWEEN_PROVIDER_CHECKS,
    SOURCE_OF_TRUTH,
    STAKERS,
)
WARNING, DANGER = BLOCK_THRESHOLDS["warning"], BLOCK_THRESHOLDS["danger"]

use_pagerduty = False

truth = {"url": SOURCE_OF_TRUTH, "nickname": "truth"}

# keep track of stakers still within the repeat_alert threshold
recently_alerted = {}

# keep last run of staker check to compare for time out of sync
previous_run = []

table, connection, metadata = connect_to_db()

def main_event(previous_run, recently_alerted):
    stakers = []
    for k, v in STAKERS.items():
        staker_data = { "url": v }
        staker_data["nickname"] = k
        stakers.append(staker_data)
    # get info from truth provider
    truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])
    truth["time_stamp"] = format_datetime(datetime.now())
    truth["blocks_out_of_sync"] = 0
    truth["ui_background"] = "bg-primary"

    # get info from stakers
    for staker in stakers:
        staker["connected"], staker["chain_id"], staker["latest_block"] = get_chain_info(staker["url"])
        staker["time_stamp"] = format_datetime(datetime.now())
        if staker["connected"]:
            staker["blocks_out_of_sync"] = int(truth["latest_block"]) - int(staker["latest_block"])
            staker["ui_background"] = set_ui_background(staker["blocks_out_of_sync"]) 

            # determine time out of sync
            if staker["blocks_out_of_sync"] < WARNING:
                staker["last_time_in_sync"] = staker["time_stamp"]
                staker["time_out_of_sync"] = format_datetime(timedelta(0))
            elif previous_run:
                last_time_in_sync = filter(lambda x: x['nickname'] == staker["nickname"], previous_run)["last_time_in_sync"]

                staker["last_time_in_sync"] = last_time_in_sync

                time_diff_since_last = datetime.strptime(staker["time_stamp"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(last_time_in_sync, "%Y-%m-%d %H:%M:%S") 
                staker["time_out_of_sync"] = format_datetime(time_diff_since_last)
            else:
                staker["last_time_in_sync"] = format_datetime(datetime.min)
            
        else:
            staker["blocks_out_of_sync"] = 'unknown'
            staker["ui_background"] = set_ui_background(DANGER)
            staker["last_time_in_sync"] = format_datetime(datetime.min)

        
    previous_run = stakers.copy()
    stakers.append(truth)

    str_stakers = str(stakers)
    dict_stakers = [{'providers_blob': str_stakers}]
    write_to_db(table, connection, metadata, dict_stakers)

    
    # TODO determine if stakers are out of sync & send alerts
    # for x in stakers[0]: print(x, flush=True) 
    # print(f'{stakers=}', flush=True)

starttime = time()
while True:
    print("tick", flush=True)
    main_event(previous_run, recently_alerted)
    sleep(SECONDS_BETWEEN_PROVIDER_CHECKS - ((time() - starttime) % SECONDS_BETWEEN_PROVIDER_CHECKS))
