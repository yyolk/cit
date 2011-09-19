#!/usr/bin/python
# -*- coding: utf-8 -*-

import user
import connect

def get_info(api_token):
    json_data, status, response = connect.connect(url="getProjects", params={'token': api_token})

    json_projects = [project for project in json_data]

    return json_projects, status, response

    #user_id = json_data['user_id']
    #name = json_data['name']
    #color = json_data['color']
    #collapsed = json_data['collapsed']
    #item_order = json_data['item_order']
    #indent = json_data['indent']
    #cache_count = json_data['cache_count']
    #unique_id = json_data['id']

def get_project(api_token, project_id):
    params = {'token': api_token, 'project_id': project_id}
    return connect.connect(url="getProject", params=params)

def add_project(api_token, name, color=None, indent=None, order=None):
    params = {'token': api_token, 'name': name}

    if color :
        params['color'] = color
    if indent :
        params['indent'] = indent
    if order:
        params['order'] = order

    return connect.connect(url="addProject", params=params)

def update_project(api_token, project_id, name=None, color=None, indent=None):
    params = {'token': api_token, 'project_id': project_id}

    if name:
        params['name'] = name
    if color :
        params['color'] = color
    if indent :
        params['indent'] = indent

    return connect.connect(url="updateProject", params=params)

def update_project_orders(api_token, project_id, item_id_list):
    # item_id_list = [3,2,9,7]
    params = {'token': api_token, 'project_id': project_id, 'item_id_list': item_id_list}
    return connect.connect(url="updateProjectOrders", params=params)

def delete_project(api_token, project_id):
    params={'token': api_token, 'project_id': project_id}
    return connect.connect(url="deleteProject", params=params)

