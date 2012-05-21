#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import connect

def query(api_token, queries):
    #TODO queries should be set by default to the users settings
    params={'token': api_token, 'ids': ids}

    if as_count :
        params['as_count'] = as_count

    if js_date :
        params['js_date'] = js_date

    json_data, status, response = connect.connect(url="query", params=params)
    return json_data, status, response
