#!/usr/bin/python3
# -*- coding: utf-8 -*-

import http.client
import urllib.request, urllib.parse, urllib.error
import json

def connect(method="GET", url='', params={}, ssl=False):
    if ssl:
        connection = http.client.HTTPSConnection("todoist.com")
    else:
        connection = http.client.HTTPConnection("todoist.com")

    return send_request(connection, method, url, params)

def send_request(connection, method, url, params):
    dest = "/API/" + url + "?" + urllib.parse.urlencode(params)

    if method == "POST" or method == "PUT":
        connection.request(method, dest, "", {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json", "Content-Length": "0"})
    else:
        connection.request(method, dest)

    response = connection.getresponse()

    if response.status == 200:
        try:
            return json.loads(response.read()) , response.status, response.reason
        except ValueError:
            return ""
    #TODO: remove response prints at release, as they interrupt user experience
    else:
        print(response.status, response.reason)





