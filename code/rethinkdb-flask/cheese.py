
import json

from flask import Flask, g,  render_template, abort

import rethinkdb as r
from rethinkdb.errors import RqlDriverError

# Configure the connection
RDB_HOST = '50.116.0.34'
RDB_PORT = 28015
DB = 'CheeseFlask'

# Setup Flask
app = Flask(__name__)
app.config.from_object(__name__)


# Connect before a request
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=DB)
    except RqlDriverError:
        abort(503, "No database connection could be established.")


# Teardown
@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


# GET ALL /cheese
@app.route('/cheese', methods=['GET'])
def get_cheese():
    cheese_options = list(r.table('Cheese').run(g.rdb_conn))
    return json.dumps(cheese_options)


# GET BY ID /cheese/id
@app.route('/cheese/<string:cheese_id>', methods=['GET'])
def get_cheese_by_id(cheese_id):
    cheese = r.table('Cheese').get(cheese_id).run(g.rdb_conn)
    return json.dumps(cheese)


# Default Route
@app.route("/", methods=['GET'])
def index():
    return render_template('cheese.html', all_cheese=list(r.table('Cheese').run(g.rdb_conn)))

if __name__ == '__main__':
    app.run(debug=True)
