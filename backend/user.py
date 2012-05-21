#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import connect

class User:
    def __init__(self, email, password):
        params={'email': email, 'password': password}
        json_data, status, response = connect.connect(url="login", params=params, ssl=True)

        self.unique_id = json_data['id']
        self.api_token = json_data['api_token']
        self.email = json_data['email']
        self.full_name = json_data['full_name']
        self.start_page = json_data['start_page']

        self.timezone = json_data['timezone']
        self.tz_offset = json_data['tz_offset']
        self.time_format = json_data['time_format']
        self.date_format = json_data['date_format']
        self.sort_order = json_data['sort_order']

        self.notifo = json_data['notifo']
        self.mobile_number = json_data['mobile_number']
        self.mobile_host = json_data['mobile_host']

        self.premium_until = json_data['premium_until']
        self.default_reminder = json_data['default_reminder']

def get_timezones():
    json_data, status, response = connect.connect(url="getTimezones", params={})
    return json_data, status, response

def register(email, full_name, password, timezone):
    if len(password) < 5:
        return "Password should be at least 5 characters long"

    params={'email': email, 'full_name': full_name, 'password': password, 'timezone':timezone}
    json_data, status, response = connect.connect(url="register", params=params, ssl=True)
    return json_data, status, response

def update_user(api_token, email=None, full_name=None, password=None, timezone=None):
    params={'api_token': api_token}

    if email :
        params['email'] = email
    if full_name :
        params['full_name'] = full_name
    if password:
        params['password'] = password
    if timezone:
        params['timezone'] = timezone

    json_data, status, response = connect.connect(url="updateUser", params=params, ssl=True)
    return json_data, status, response



