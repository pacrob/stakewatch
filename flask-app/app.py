from datetime import datetime, timedelta
from tkinter import W
from weakref import proxy
from flask import Flask, render_template

from config import (
    BLOCK_THRESHOLDS,
    SOURCE_OF_TRUTH,
    STAKERS,
    TIME_THRESHOLDS,
)

app = Flask(__name__)

# setup
# WARNING, DANGER = BLOCK_THRESHOLDS["warning"], BLOCK_THRESHOLDS["danger"]
# START_TIME = datetime.now()
# truth = {"url": SOURCE_OF_TRUTH}

stakers = []
for k, v in STAKERS.items():
    staker_data = { "url": v }
    staker_data["nickname"] = k
    staker_data["in_sync"] = False
    staker_data["time_out_of_sync"] = timedelta(0)
    stakers.append(staker_data)

import sqlalchemy as db



def read_from_db():
    print('running read_from_db', flush=True)
    engine = db.create_engine('sqlite:////db/stakewatch.db?'
                              'check_same_thread=false')
    connection = engine.connect()
    metadata = db.MetaData()
    stakewatch = db.Table('stakewatch', metadata, autoload=True, autoload_with=engine)

    def run_query(query):
        proxy_result = connection.execute(query)
        result = proxy_result.fetchall()
        return result


    max_id_query = db.select([db.func.sum(stakewatch.c.id)])
    max_id_return = run_query(max_id_query)
    max_id = max_id_return[0][0]  # max_id_return is a list of a tuple
    print(f'{max_id=}', flush=True)

    #most_recent_2_query = db.select([stakewatch].where)
    
    #query = db.select([stakewatch.c.nickname.distinct()])

    # with engine.connect() as conn:
    #     result = conn.execute(
    #         # db.select([stakewatch.c.nickname.distinct()])
    #         db.select([stakewatch])
    #     )
            
    #     print(result, flush=True)
    result = 'pants'    
    print(result, flush=True)
    # inst = db.inspect(stakewatch)
    # attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    # print(f'{attr_names=}')
    # query = db.select([stakewatch]).order_by(stakewatch.c.id.desc()).limit(5)
    # max_id_query = db.select([db.func.max(stakewatch.columns.id)])
    # max_proxy = connection.execute(max_id_query)
    # max_result = max_proxy.fetchall()

    # print(f'{max_result=}')
    # s = stakewatch.select()
    # # conn = engine.connect()
    # result = connection.execute(s)

    # # query = db.select([stakewatch])
    # # ResultProxy = connection.execute(query)
    # # result = ResultProxy.fetchall()

    # for x in result:
    #     # d = {}
    #     print('am here')
    #     print('type of result = ', type(result))
    #     print(x)

    # convert db data to dict
    
    truth = 'hello'
    stakers = ['hello', 'hello']
    return truth, stakers, result
    # truth["connected"], truth["chain_id"], truth["latest_block"] = get_chain_info(truth["url"])
    # current_time = datetime.now()
    # alerts_to_send = []

    # for staker in stakers:
    #     staker["connected"], staker["chain_id"], staker["latest_block"] = get_chain_info(staker["url"])
        
    #     if staker["connected"] and truth["connected"]:
    #         block_diff = truth["latest_block"] - staker["latest_block"]
    #         if block_diff > DANGER:
    #             staker["background"] = "bg-danger"
    #             staker["in_sync"] = False
    #             staker["time_out_of_sync"] = current_time - staker["last_time_in_sync"]
    #         elif block_diff > WARNING:
    #             staker["background"] = "bg-warning"
    #             staker["in_sync"] = False
    #             staker["time_out_of_sync"] = current_time - staker["last_time_in_sync"]
    #         else:
    #             staker["background"] = "bg-success"
    #             staker["last_time_in_sync"] = current_time
    #             staker["in_sync"] = True

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

    # sleep(30)
    # update_staker_info()




# end sleep loop

# this route does not automatically refresh
@app.route("/")
def index():

    truth, stakers, result = read_from_db()
    print('now down here', result, flush=True)

    now = datetime.now()
    return render_template(
        "index.html",
        source_of_truth = truth,
        stakers = stakers,
        time = now,
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
