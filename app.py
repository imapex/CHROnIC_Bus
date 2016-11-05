from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from flask_dataset import Dataset
import json, requests

app = Flask(__name__)
app.config['DATASET_DATABASE_URI'] = 'sqlite:///:memory:'
db = Dataset(app)

@app.route('/', methods=['GET'])
def return_blank():
    return ""

@app.route('/api/send/<collectorid>', methods=['DELETE'])
def clear_bus(collectorid):
    with app.test_request_context():
        retval = db['msgbus'].delete(colid=collectorid)
    resp = Response("", status=204, mimetype='application/json')
    return resp

@app.route('/api/send/<collectorid>', methods=['POST'])
def send_message(collectorid):
    content = request.json
    content['colid'] = collectorid
    with app.test_request_context():
        retval = db['msgbus'].insert(content)
    text = str(retval)
    return text

@app.route('/api/get/<collectorid>', methods=['GET'])
def get_message(collectorid):
    table = db['msgbus']
    messages = table.find(colid=collectorid)
    arr_messages = []
    for message in messages:
        arr_messages.append(json.loads(json.dumps(message)))
        UpdateStatus(message, 1)
        #thisid = message['id']
        #res = db.query('UPDATE msgbus SET status="1" WHERE id="' + str(thisid) + '"')
    text = json.dumps(arr_messages) 
    return text

def UpdateStatus(message, newstatus):
    messageid = message['id']
    url = ""
    if 'webhook' in message:
        url = message['webhook']

    headers = {
        'content-type': 'application/json'
    }
    hookdata = {"id": str(messageid), "status": str(newstatus)}
    jsondata = json.dumps(hookdata)

    res = db.query('UPDATE msgbus SET status="' + str(newstatus) + '" WHERE id="' + str(messageid) + '"')
    if url != "":
        response = requests.request("POST", url, data=jsondata, headers=headers)

if __name__ == '__main__':
    # Run Flask
    app.run(debug=True, host='0.0.0.0', port=int("5000"))
    # pass

