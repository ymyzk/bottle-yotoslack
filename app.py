#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from os import path

import bottle
from bottle import abort, request
import requests


app = bottle.default_app()
app.config.load_config("app.conf")


@app.route(app.config["yo.callback_url"])
def index():
    # Parse query
    user_ip = request.query.user_ip
    username = request.query.username
    link = request.query.link
    location = request.query.location

    # Query validation
    if user_ip == "" or username == "":
        return abort(400)

    # Message generation
    message = "Yo from " + username

    if link != "":
        message += "\n" + link

    if location != "":
        lat, lng = map(float, location.split(";"))
        message += "\nhttps://www.google.co.jp/maps/"
        message += "@{lat},{lng},{zoom}z".format(lat=lat, lng=lng, zoom=17)

    # Slack notification
    payload = {
        "channel": app.config["slack.channel"],
        "text": message
    }

    data = {
        "payload": json.dumps(payload)
    }

    requests.post(app.config["slack.webhook_url"], data=data)

    # Dummy response
    return { "result": "ok" }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
else:
    application = app
