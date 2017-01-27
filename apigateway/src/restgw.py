from flask import Flask
from flask import request
from flask import jsonify

import requests
import json
import os

app = Flask(__name__)

@app.route("/")
def get_root_info():
    return jsonify ( { 'TODO': "give more details about apis" } ) 

@app.route("/railsapp/")
def call_railsapp():
    response = requests.get(os.environ['RAILSAPP_URL'] + '/json')
    if response.status_code == 200 :
        return jsonify(response.json())

    return jsonify ( { 'ResponseStatusCode': response.status_code } ) 

@app.route("/flaskapp/")
def call_flaskapp():
    response = requests.get(os.environ['FLASKAPP_URL'] + '/json')
    if response.status_code == 200 :
        return jsonify(response.json())

    return jsonify ( { 'ResponseStatusCode': response.status_code } ) 

@app.route("/pythonapp/")
def call_pythonapp():
    response = requests.get(os.environ['PYTHONAPP_URL'] + '/json')
    if response.status_code == 200 :
        return jsonify(response.json())

    return jsonify ( { 'ResponseStatusCode': response.status_code } ) 

    
if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')
