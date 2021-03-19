#!/bin/env python3

import signal
import sys
import os
import argparse
import shutil
import sys
import queue
import json
import bottle
from bottle import run, route, template, get, post, request, redirect, static_file, hook, response

app = bottle.app()
app.catchall = False

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

event_dataQ = queue.Queue()
metric_dataQ = queue.Queue()

@hook('after_request')
def setup_response():
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    response.headers['Content-Type'] = 'application/json; charset=UTF-8'


@get('/event')
def get_event():
    req_data = None

    response = event_dataQ.get() if event_dataQ.empty() is False else {}

    return json.dumps(response)

@post('/event')
def post_event():
    req_data = None
    context = request.body.read().decode('utf-8')
    print("POST: {}".format(context))
    if context != "" and context != None:
        req_data = json.loads(context)
        event_dataQ.put(req_data)

    response = {}

    return json.dumps(response)

@get('/metric_event')
def get_metric_event():
    req_data = None

    response = metric_dataQ.get() if metric_dataQ.empty() is False else {}

    return json.dumps(response)

@post('/metric_event')
def post_metric_event():
    req_data = None
    context = request.body.read().decode('utf-8')
    print("POST: {}".format(context))
    if context != "" and context != None:
        req_data = json.loads(context)
        metric_dataQ.put(req_data)

    response = {}

    return json.dumps(response)


def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server_port', type=str, default='5000', help='server port')
    return parser.parse_args()

def main():
    args = process_command()
    run(app=app, host='0.0.0.0', port=args.server_port)


if __name__ == "__main__":
    main()

