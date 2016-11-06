from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from flask_dataset import Dataset
import json, requests

app = Flask(__name__)
app.config['DATASET_DATABASE_URI'] = 'sqlite:///:memory:'
#app.config['DATASET_SCHEMA'] = 
db = Dataset(app)

@app.route('/', methods=['GET'])
def return_blank():
    return ""

@app.route('/api/status/<taskid>', methods=['GET'])
def get_status(taskid):
    table = db['msgbus']
    messages = table.find(id=taskid)
    mcount = table.count(id=taskid)
    resp = ""
    if mcount == 0:
        resp = Response("", status=404, mimetype='application/json')
    else:
        arr_messages = []
        for message in messages:
            arr_messages.append(json.loads(json.dumps(message)))
        resp = json.dumps(arr_messages)
    return resp

@app.route('/api/status/<taskid>', methods=['POST'])
def update_task(taskid):
    content = request.json
    #print(content)
    newstatus = content['status']
    resp = ""
    with app.test_request_context():
        #data = dict(id=taskid, status=newstatus)
        #retval = db['msgbus'].update(data, ['id'])
        message = db['msgbus'].find_one(id=taskid)
        print(message)
        if message != None:
            retval = UpdateStatus(message, newstatus)
            #print(retval)
        else:
            retval = 0
        if retval == 0:
            resp = Response("", status=404, mimetype='application/json')
        else:
            resp = Response("", status=200, mimetype='application/json')
    return resp

@app.route('/api/send/<collectorid>', methods=['DELETE'])
def clear_bus(collectorid):
    resp = Response("", status=204, mimetype='application/json')
    with app.test_request_context():
        mcount = db['msgbus'].count(colid=collectorid)
        if mcount == 0:
            resp = Response("", status=404, mimetype='application/json')
        else:
            retval = db['msgbus'].delete(colid=collectorid)
    #resp = Response("", status=204, mimetype='application/json')
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
    mcount = db['msgbus'].count(colid=collectorid)
    if mcount == 0:
        resp = Response("", status=404, mimetype='application/json')
    else:
        arr_messages = []
        for message in messages:
            arr_messages.append(json.loads(json.dumps(message)))
            UpdateStatus(message, 1)
        resp = json.dumps(arr_messages) 
    return resp

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

    data = dict(id=messageid, status=newstatus)
    retval = db['msgbus'].update(data, ['id'])
    #res = db.query('UPDATE msgbus SET status="' + str(newstatus) + '" WHERE id="' + str(messageid) + '"')
    if url != "":
        response = requests.request("POST", url, data=jsondata, headers=headers)

    return retval

if __name__ == '__main__':
    # Run Flask
    app.run(debug=True, host='0.0.0.0', port=int("5000"))
    # pass

