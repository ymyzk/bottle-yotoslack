#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hashlib import md5

import bottle
from bottle import abort, request
from channels.backends.slack import SlackChannel
import requests


app = bottle.default_app()
app.config.load_config("app.conf")

colors = [
    "#1ABC9C",
    "#2ECC71",
    "#3498DB",
    "#34495E",
    "#16A085",
    "#F1C40F",
    "#2980B9",
    "#8E44AD"
]

@app.route(app.config["yo.callback_url"])
def index():
    # Parse query
    username = request.query.username
    link = request.query.link
    location = request.query.location

    # Query validation
    if username == "":
        return abort(400)

    # Message generation
    color = colors[int(md5(username.encode("utf-8")).hexdigest(), 16)
                   % len(colors)]
    attachments = [
        {
            "color": color,
            "fields": []
        }
    ]

    message = "Yo{type} from " + username

    if link != "":
        message = message.format(type=" Link")
        attachments[0]["fields"].append({
            "title": "Link",
            "value": link,
            "short": False
        })
    elif location != "":
        message = message.format(type=" Location")
        coordinate = location.replace(";", ",")

        # Reverse geocoding
        address = reverse_geocoding(coordinate)
        if address is not None:
            attachments[0]["fields"].append({
                "title": "Address",
                "value": address,
                "short": True
            })

        # Google Maps Link
        attachments[0]["fields"].append({
            "title": "Google Maps",
            "value": get_map_link(coordinate),
            "short": True
        })

        # Static map
        attachments[0]["image_url"] = get_static_map_url(coordinate)
    else:
        message = message.format(type="")

    attachments[0]["fallback"] = message
    attachments[0]["text"] = message

    # Slack notification
    slack = SlackChannel(url=app.config["slack.webhook_url"],
                         username="Yo",
                         channel=app.config["slack.channel"])

    slack.send("", options={
        "slack": {
            "attachments": attachments,
            "unfurl_links": True
        }
    })

    # Dummy response
    return {"result": "ok"}


def get_map_link(coordinate, zoom=15):
    return "https://www.google.co.jp/maps/@{coordinate},{zoom}z".format(
        coordinate=coordinate,
        zoom=zoom)


def get_static_map_url(coordinate, zoom=16):
    params = {
        "center": coordinate,
        "zoom": zoom,
        "format": "png",
        "sensor": "false",
        "size": "640x640",
        "maptype": "roadmap",
        "markers": coordinate
    }
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    url += "&".join([k + "=" + str(v) for k, v in params.items()])
    return url


def reverse_geocoding(coordinate):
    params = {
        "latlng": coordinate,
        "language": "ja",
        "sensor": "false"
    }
    url = "https://maps.googleapis.com/maps/api/geocode/json"

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


def shorten_url(long_url, fail_silently=True):
    try:
        params = {
            "access_token": app.config["bitly.token"],
            "longUrl": long_url
        }
        url = "https://api-ssl.bitly.com/v3/shorten"
        response = requests.get(url, params=params)
        assert response.status_code == 200
        url = response.json()["data"]["url"]
    except:
        if fail_silently:
            url = long_url
        else:
            raise

    return url


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)
else:
    application = app
