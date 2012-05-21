#!/usr/bin/python3
# -*- coding: utf-8 -*-
from . import connect

def add_note(api_token, item_id, content):
    params={'token': api_token, 'item_id': item_id, 'content': content}

    json_data, status, response = connect.connect(url="addNote", params=params)
    return json_data, status, response

def delete_note(api_token, item_id, note_id):
    params={'token': api_token, 'item_id': item_id, 'note_id': note_id}

    json_data, status, response = connect.connect(url="deleteNote", params=params)
    return json_data, status, response

def get_notes(api_token, item_id):
    params={'token': api_token, 'item_id': item_id}

    json_data, status, response = connect.connect(url="getNotes", params=params)
    return json_data, status, response
