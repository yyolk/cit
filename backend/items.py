#!/usr/bin/python
# -*- coding: utf-8 -*-

import connect

def get_uncompleted_items(api_token, project_id, js_date=None):
    params={'token': api_token, 'project_id': project_id}

    if js_date :
        params['js_date'] = js_date

    return connect.connect(url="getUncompletedItems", params=params)

def get_completed_items(api_token, project_id, js_date=None):
    params={'token': api_token, 'project_id': project_id}

    if js_date :
        params['js_date'] = js_date

    return connect.connect(url="getCompletedItems", params=params)

def get_items_by_id(api_token, ids, js_date=None):
    #ids contains a list of items id's
    params={'token': api_token, 'ids': ids}

    if js_date :
        params['js_date'] = js_date

    return connect.connect(url="getItemsById", params=params)

def add_item(api_token, project_id, content, date_string=None, priority=None, js_date=None):
    params={'token': api_token, 'project_id': project_id, 'content': content}

    if date_string :
        params['date_string'] = date_string

    if priority :
        params['priority'] = priority

    if js_date :
        params['js_date'] = js_date

    return connect.connect(url="addItem", params=params)

def update_item(api_token, item_id,
               content=None, date_string=None, priority=None,
               indent=None, item_order=None, js_date=None):

    params={'token': api_token, 'id': item_id}

    if content :
        params['content'] = content

    if date_string :
        params['date_string'] = date_string

    if priority :
        params['priority'] = priority

    if indent :
        params['indent'] = indent

    if item_order :
        params['item_order'] = item_order

    if js_date :
        params['js_date'] = js_date

    return connect.connect(url="updateItem", params=params)

def update_orders(api_token, project_id, item_id_list):
    params={'token': api_token, 'project_id': project_id, 'item_id_list': item_id_list}

    return connect.connect(url="updateOrders", params=params)

def update_recurring_date(api_token, ids):
    params={'token': api_token, 'ids': ids}

    if js_date :
        params['js_date'] = js_date

    return connect.connect(url="updateRecurringDate", params=params)

def delete_items(api_token, ids):
    params={'token': api_token, 'ids': ids}

    return connect.connect(url="deleteItems", params=params)

def complete_items(api_token, ids):
    params={'token': api_token, 'ids': ids}

    if in_history :
        params['in_history'] = in_history

    return connect.connect(url="completeItems", params=params)

def uncomplete_items(api_token, ids):
    params={'token': api_token, 'ids': ids}

    return connect.connect(url="uncompleteItems", params=params)
