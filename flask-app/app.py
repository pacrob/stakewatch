from datetime import datetime, timedelta
from tkinter import W
from weakref import proxy
from flask import Flask, render_template

import operator

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


    max_id_query = db.select([db.func.max(stakewatch.c.id)])
    max_id_return = run_query(max_id_query)
    max_id = max_id_return[0][0]  # max_id_return is a list of a tuple
    print(f'{max_id=}', flush=True)
    print(type(max_id), flush=True)
    
    top_ten_query = db.select([stakewatch]).where(stakewatch.c.id > (max_id - 10))
    top_ten_return = run_query(top_ten_query)
    # print(f'{top_ten_return=}')
    # for x in top_ten_return:
    #     print(x[2:5], flush=True) 
        
    def parse_db_rows(rows):
        # rows is a list of db rows as tuples
        keys = ['id', 'url', 'nickname', 'connected', 'chain_id', 'latest_block', 'time_stamp']
        records = []
        for row in rows:
            new_record = {}
            for idx, key_name in enumerate(keys):
                new_record[key_name] = row[idx]

            records.append(new_record)
        
        return records

    parsed_rows = parse_db_rows(top_ten_return) 

    sorted_rows = sorted(parsed_rows, key=(operator.itemgetter("time_stamp")))
    # for x in sorted_rows:
    #     print(x["time_stamp"], flush=True) 
        
    unique_stakers = set()
    most_recent_rows = []
    for x in sorted_rows:
        if x['nickname'] not in unique_stakers:
            unique_stakers.add(x['nickname'])
            most_recent_rows.append(x)

    print(most_recent_rows, flush=True)
    truth = list(filter(lambda x: x['nickname'] == 'truth', most_recent_rows))
    stakers = list(filter(lambda x: x['nickname'] != 'truth', most_recent_rows))
    print(f'{truth=}', flush=True)
    print(f'{stakers=}', flush=True)
    
    return truth[0], stakers

# this route does not automatically refresh
@app.route("/")
def index():

    truth, stakers = read_from_db()

    now = datetime.now()
    return render_template(
        "index.html",
        source_of_truth = truth,
        stakers = stakers,
        time = now,
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
