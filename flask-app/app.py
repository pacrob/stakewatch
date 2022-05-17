from datetime import datetime, timedelta
from flask import Flask, render_template
import json

app = Flask(__name__)

stakers = []

import sqlalchemy as db



def read_from_db():
    engine = db.create_engine('sqlite:////db/stakewatch.db?'
                              'check_same_thread=false')
    connection = engine.connect()
    metadata = db.MetaData()
    stakewatch = db.Table('stakewatch', metadata, autoload=True, autoload_with=engine)

    def run_query(query):
        proxy_result = connection.execute(query)
        result = proxy_result.fetchall()
        return result

    # get the most recent staker info from the database
    max_id_query = db.select([db.func.max(stakewatch.c.id)])
    max_id_return = run_query(max_id_query)
    max_id = max_id_return[0][0]
    latest_row_query = db.select([stakewatch]).where(stakewatch.c.id == max_id)
    latest_row = run_query(latest_row_query)
    json_string = latest_row[0][1]
    
    # parse the row to a list of dicts
    json_string = json_string.replace("\'", "\"")
    list_of_stakers = json.loads(json_string)
    truth = list(filter(lambda x: x['nickname'] == 'truth', list_of_stakers))
    stakers = list(filter(lambda x: x['nickname'] != 'truth', list_of_stakers))
    
    return truth[0], stakers

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
