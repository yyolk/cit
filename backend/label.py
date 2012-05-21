#!/usr/bin/python3
# -*- coding: utf

from . import connect

def get_labels(token):
    params={'token': token}
    json_data, status, response = connect.connect(url="getLabels", params=params)
    return json_data, status, response

def update_label(token, old_name, new_name):
    params={'token': token, 'old_name': old_name, 'new_name':new_name}
    json_data, status, response = connect.connect(url="updateLabel", params=params)
    return json_data, status, response

def delete_label(token, name):
    params = {'token': token, 'name': name}
    json_data, status, response = connect.connect(url="deleteLabel", params=params)
    return json_data, status, response



