#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def tear_down(self):
    """closes the storage"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    """display a HTML page"""
    states_o = [x for x in storage.all("State").values()]
    return render_template('7-states_list.html',
                           states_o=states_o)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
