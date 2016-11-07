#!/usr/bin/python
from flask import Flask, request, Response
from flask_dataset import Dataset
import json
import requests

# -- Application Setup
app = Flask(__name__)
app.config['DATASET_DATABASE_URI'] = 'sqlite:///:memory:'
db = Dataset(app)


# -- Add default route (/) for basic health check
@app.route('/', methods=['GET'])
def return_blank():
    return ""


# -- Add route to GET status for a task
@app.route('/api/status/<taskid>', methods=['GET'])
def get_status(taskid):
    table = db['msgbus']
    messages = table.find(id=taskid)
    mcount = table.count(id=taskid)
    resp = ""
    if mcount == 0:
        # If there is not a task with the specified ID, return 404
        resp = Response("", status=404, mimetype='application/json')
    else:
        # Loop through tasks (should only be one), add to json array
        arr_messages = []
        for message in messages:
            arr_messages.append(json.loads(json.dumps(message)))
        resp = json.dumps(arr_messages)
    return resp


# -- Add route to POST new status for a task
@app.route('/api/status/<taskid>', methods=['POST'])
def update_task(taskid):
    content = request.json
    newstatus = content['status']
    resp = ""
    with app.test_request_context():
        message = db['msgbus'].find_one(id=taskid)
        # If the task exists, perform an update
        if message is not None:
            retval = UpdateStatus(message, newstatus)
        else:
            retval = 0
        if retval == 0:
            # If the task does not exist, or if there was a problem, return 404
            resp = Response("", status=404, mimetype='application/json')
        else:
            # Return 200 ok
            resp = Response("", status=200, mimetype='application/json')
    return resp


# -- Add route to DELETE all tasks for a specified collector
@app.route('/api/send/<collectorid>', methods=['DELETE'])
def clear_bus(collectorid):
    # Default return 204 deleted
    resp = Response("", status=204, mimetype='application/json')
    with app.test_request_context():
        mcount = db['msgbus'].count(colid=collectorid)
        # If there are no tasks for the specified collector, return 404
        if mcount == 0:
            resp = Response("", status=404, mimetype='application/json')
        else:
            db['msgbus'].delete(colid=collectorid)
    return resp


# -- Add route to POST new task for a specified collector
@app.route('/api/send/<collectorid>', methods=['POST'])
def send_message(collectorid):
    content = request.json
    content['colid'] = collectorid
    # Add new task to the queue for the specified collector
    with app.test_request_context():
        retval = db['msgbus'].insert(content)
    text = str(retval)
    return text


# -- Add route to GET all tasks for specified collector
@app.route('/api/get/<collectorid>', methods=['GET'])
def get_message(collectorid):
    table = db['msgbus']
    messages = table.find(colid=collectorid)
    mcount = db['msgbus'].count(colid=collectorid)
    # If there are no tasks for the specified collector, return 404 not found
    if mcount == 0:
        resp = Response("", status=404, mimetype='application/json')
    else:
        # If there are tasks, loop through and dump in json array
        arr_messages = []
        for message in messages:
            arr_messages.append(json.loads(json.dumps(message)))
            UpdateStatus(message, 1)
        resp = json.dumps(arr_messages)
    return resp


# -- Function used to update status on a task - used when manual task update is
# POSTed or when a GET is done for all tasks
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
    # if a webhook was specified, call the webhook since there was an update
    if url != "":
        requests.request("POST", url, data=jsondata, headers=headers)
    return retval


# -- Main function
if __name__ == '__main__':
    # Run Flask
    app.run(debug=True, host='0.0.0.0', port=int("5000"))
