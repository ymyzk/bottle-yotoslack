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
    if username == "":
        return abort(400)

    # Message generation
    message = "Yo{type} from " + username

    if link != "":
        message = message.format(type=" Link")
        message += "\n" + link
    elif location != "":
        message = message.format(type=" Location")
        coordinate = location.replace(";", ",")

        # Reverse geocoding
        address = reverse_geocoding(coordinate)
        if address is not None:
            message += "\n" + address

        # Google Maps Link
        message += "\nhttps://www.google.co.jp/maps/"
        message += "@{coordinate},15z".format(coordinate=coordinate)

        # Static map
        params = {
            "center": coordinate,
            "zoom": 16,
            "format": "png",
            "sensor": "false",
            "size": "640x640",
            "maptype": "roadmap",
            "markers": coordinate
        }
        message += "\nhttp://maps.googleapis.com/maps/api/staticmap?"
        message += "&".join([k + "=" + str(v) for k, v in params.items()])
    else:
        message = message.format(type="")


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


def reverse_geocoding(coordinate):
    params = {
        "latlng": coordinate,
        "language": "ja",
        "sensor": "false"
    }
    url = "http://maps.googleapis.com/maps/api/geocode/json"

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return

    json = response.json()
    if json["status"] != "OK":
        return

    results = json["results"]
    if len(results) == 0:
        return

    components = results[0]["address_components"]
    required = [
        "administrative_area_level_1",
        "locality",
        "sublocality_level_1"
    ]

    result = ""
    for component in reversed(components):
        if len([c for c in component["types"] if c in required]) > 0:
            result += component["long_name"]

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)
else:
    application = app
