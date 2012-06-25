#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
import ConfigParser
import textwrap

import backend.user
import backend.project
import backend.items

conf_file = os.path.expanduser("~/.citrc")
project_file = os.path.expanduser("~/.citproject")
task_file = os.path.expanduser("~/.cittask")

def main(args):

    # Configuration file must exist before we continue
    if not os.path.exists(conf_file):
        try:
            save_info(args.save_info)
        except:
            return "Before you continue enter your loging credentials\n" \
                   "usage: ./cit.py save -i <email> <password>"

    if args.add:
        add_item(args.add)
    # add_project is None by default
    elif args.add_project is not None:
        # Check for empty string
        if not args.add_project:
            print "Please define project"
            return
        else:
            add_project(args.add_project)

    if args.ls:
        list_project_items(args.ls)
    elif args.ls is not None:
        # If no arguments are given show all items
        list_all_items()

    if args.projects:
        print "You probably want to run 'cit projects'"
        pass
    elif args.projects is not None:
        list_projects()



    if args.rm:
        delete_items(args.rm)
    # add_project is None by default
    elif args.delete_project is not None:
        # Check for empty string
        if not args.delete_project:
            print "Please define project"
            return
        else:
            delete_project(args.delete_project)

    if args.rename_project is not None:
        if len(args.rename_project) is not 3:
            print "Please seperate the projects to be renamed with a comma"
            print
            print "Example: cit up -p old_project, new_project"
            return
        else:
            rename_project(args.rename_project)
        # Check for empty string
    elif args.up:
        pass
    elif args.up is not None:
        print "Options are..."


    if not args.save:
        if args.save_info:
            save_info(args.save_info)
            save_projects()
            save_items()
        elif args.save_all:
            save_projects()
            save_items()
    else:
        print "Options are..."

def save_info(save_user_args):
    username = save_user_args[0]
    password = save_user_args[1]

    user = backend.user.User(username, password)

    config = ConfigParser.RawConfigParser()
    config.add_section('user_info')
    config.set('user_info', 'username', username)
    config.set('user_info', 'password', password)
    config.set('user_info', 'full_name', user.full_name)
    config.set('user_info', 'id', user.unique_id)
    config.set('user_info', 'api_token', user.api_token)
    config.set('user_info', 'start_page', user.start_page)

    config.set('user_info', 'timezone', user.timezone)
    config.set('user_info', 'tz_offset', user.tz_offset)
    config.set('user_info', 'time_format', user.time_format)

    config.set('user_info', 'date_format', user.date_format)
    config.set('user_info', 'sort_order', user.sort_order)

#TODO: find a way to test user for premium subscription
#    config.set('user_info', 'notifo', user.notifo)
#    config.set('user_info', 'premium_until', user.premium_until)
#    config.set('user_info', 'default_reminder', user.default_reminder)

    with open(conf_file, 'wb') as configfile:
        config.write(configfile)

def colorize(msg, color, nocolor=False):
    """Colorizes the given message."""
    # The nocolor is added to shut off completely. You may ask the point of this
    # someone want to pipe the output, but the asci characters will also printed
    if nocolor:
        return msg
    else:
        colors = {'green'   : '\x1b[32;01m%s\x1b[0m',
                  'red'     : '\x1b[31;01m%s\x1b[0m',
                  'yellow'  : '\x1b[33;01m%s\x1b[0m',
                  'bold'    : '\x1b[1;01m%s\x1b[0m',
                  'none'    : '\x1b[0m%s\x1b[0m',
                 }
        return colors[color if sys.stdout.isatty() else 'none'] % msg


def save_items():
    if os.path.exists(task_file):
        os.remove(task_file)

    conf = GetUserInfo()
    token = conf.api_token
    config_project = ConfigParser.RawConfigParser()
    config_project.read(project_file)
    config_task = ConfigParser.RawConfigParser()
    config_task.read(task_file)

    for project_id in config_project.sections():
        json_projects, status, response = backend.items.get_uncompleted_items(token, project_id)

        for task_dict in json_projects:
            #Fix unicode problem
            safe_str = task_dict['content'].encode('ascii', 'ignore')

            config_task.add_section(str(task_dict['id']))
            config_task.set(str(task_dict['id']), 'id', task_dict['id'])
            config_task.set(str(task_dict['id']), 'project_id', task_dict['project_id'])
            config_task.set(str(task_dict['id']), 'content', safe_str)
            config_task.set(str(task_dict['id']), 'user_id', task_dict['user_id'])
            config_task.set(str(task_dict['id']), 'collapsed', task_dict['collapsed'])
            config_task.set(str(task_dict['id']), 'priority', task_dict['priority'])
            config_task.set(str(task_dict['id']), 'item_order', task_dict['item_order'])
            config_task.set(str(task_dict['id']), 'in_history', task_dict['in_history'])
            config_task.set(str(task_dict['id']), 'checked', task_dict['checked'])
            config_task.set(str(task_dict['id']), 'indent', task_dict['indent'])
            config_task.set(str(task_dict['id']), 'date_string', task_dict['date_string'])

        with open(task_file, 'wb') as configfile:
            config_task.write(configfile)

    print "All uncompleted tasks are downloaded and stored to %s" % task_file

def list_all_items():
    conf = GetUserInfo()
    token = conf.api_token
    config_project = ConfigParser.RawConfigParser()
    config_project.read(project_file)
    config_task = ConfigParser.RawConfigParser()
    config_task.read(task_file)

    print "Id  Project    Item"
    print "--  -------    ----"
    for id_name in config_project.sections():
        project_name = config_project.get(id_name, 'name')

        for sections in config_task.sections():
            project_id_task = config_task.get(sections, 'project_id')

            if id_name == project_id_task:
                content = config_task.get(sections, 'content')
                item_order = config_task.get(sections, 'item_order')
                indent = config_task.get(sections, 'indent')

                print item_order.rjust(2),
                print '  ' * (int(indent) - 1),
                print project_name.ljust(10),
                print content

def list_project_items(args):
    conf = GetUserInfo()
    token = conf.api_token
    config_project = ConfigParser.RawConfigParser()
    config_project.read(project_file)
    config_task = ConfigParser.RawConfigParser()
    config_task.read(task_file)

    # args = ["+work", "+personal"] --> bare_project = ["work", "personal"]
    bare_project = [arg[1:] for arg in args if arg.startswith("+")]

    for project_arg in bare_project:

        for id_name in config_project.sections():
            project_name = config_project.get(id_name, 'name')

            if project_arg == project_name:
                print_project = True
                for sections in config_task.sections():
                    project_id_task = config_task.get(sections, 'project_id')

                    if id_name == project_id_task:
                        if print_project:
                            print
                            print colorize(textwrap.fill(project_name, initial_indent='      '), "bold")
                            print colorize(textwrap.fill(('-' * len(project_name)), initial_indent='      '), "bold")
                        print_project = False
                        content = config_task.get(sections, 'content')
                        item_order = config_task.get(sections, 'item_order')
                        indent = config_task.get(sections, 'indent')

                        print "(%s)" % item_order.rjust(2),
                        print '  ' * (int(indent) - 1),
                        print textwrap.fill(content, initial_indent='', subsequent_indent='      ')

def list_projects():
    config = ConfigParser.RawConfigParser()
    config.read(project_file)

    print "Project    Items"
    print "-------    -----"

    for id_name in config.sections():
        section_name = config.get(id_name, 'name')
        indent = config.get(id_name, 'indent')
        item_order = config.get(id_name, 'item_order')
        total_items = config.get(id_name, 'cache_count')

        print section_name.ljust(10),
        print '  ' * (int(indent) - 1),
        print total_items.rjust(4)


def delete_items(args):
    conf = GetUserInfo()
    token = conf.api_token

    config_project = ConfigParser.RawConfigParser()
    config_project.read(project_file)
    config_task = ConfigParser.RawConfigParser()
    config_task.read(task_file)

    item_to_delete = []
    for arg in args:
        if arg.isdigit():
            item_to_delete.append(arg)
        elif arg.startswith("+"):
            from_project = arg[1:]
        elif isinstance(arg, str):
            from_project = arg


    obsolote_task_ids = []
    for project_id in config_project.sections():
        project_name = config_project.get(project_id, 'name')
        project_order = config_project.get(project_id, 'item_order')

        if from_project == project_name or from_project == project_order:
            for sections in config_task.sections():
                for task in item_to_delete:
                    project_id_task = config_task.get(sections, 'project_id')
                    item_order_task = config_task.get(sections, 'item_order')

                    if project_id == project_id_task and item_order_task == task:
                        print "removed section: %s" % sections
                        obsolote_task_ids.append(sections)
                        config_task.remove_section(sections) # Remove this sections

    status = backend.items.delete_items(token,json.dumps(obsolote_task_ids))
    # Write changes to file
    with open(task_file, 'wb') as configfile:
        config_task.write(configfile)

def add_item(args):
    conf = GetUserInfo()
    token = conf.api_token
    config_project = ConfigParser.RawConfigParser()
    config_project.read(project_file)

    # Filter out project names and convert the list to string
    content = [arg for arg in args if not arg.startswith("+")]
    content = " ".join(content)

    # Projects are defined via the plus sign ...  +Project1 +Example
    project = [arg[1:] for arg in args if arg.startswith("+")]
    if not project:
        print "Project is not given, append the name via a plus (+) prefix\n"
        print "Example:  cit add Take out the Trash +Personal"
        return

    # For now support add items only to "one" project
    for project_id in config_project.sections():
        project_name = config_project.get(project_id, 'name')

        if project_name == project[0]:
            status  = backend.items.add_item(token, project_id, content, None, priority="1")
            if not status:
                print "ERROR: Not able to add task to Todoist.com" % deleted
            elif status[1] == 200:
                print "Task is added to project: \"%s\"" % project_name

    # Save item to task_file
    #TODO Create a function for this kind of task
    task_dict = status[0]
    config_task = ConfigParser.RawConfigParser()
    config_task.read(task_file)
    config_task.add_section(str(task_dict['id']))
    config_task.set(str(task_dict['id']), 'id', task_dict['id'])
    config_task.set(str(task_dict['id']), 'project_id', task_dict['project_id'])
    config_task.set(str(task_dict['id']), 'content', task_dict['content'])
    config_task.set(str(task_dict['id']), 'user_id', task_dict['user_id'])
    config_task.set(str(task_dict['id']), 'collapsed', task_dict['collapsed'])
    config_task.set(str(task_dict['id']), 'priority', task_dict['priority'])
    config_task.set(str(task_dict['id']), 'item_order', task_dict['item_order'])
    config_task.set(str(task_dict['id']), 'in_history', task_dict['in_history'])
    config_task.set(str(task_dict['id']), 'checked', task_dict['checked'])
    config_task.set(str(task_dict['id']), 'indent', task_dict['indent'])
    config_task.set(str(task_dict['id']), 'date_string', task_dict['date_string'])
    with open(task_file, 'ab') as configfile:
        config_task.write(configfile)


def add_project(project_name):

    conf = GetUserInfo()
    token = conf.api_token

    project_name = " ".join(project_name)
    status = backend.project.add_project(token, project_name)

    # status has two types, the if/else condition must start with status
    # status=False , status ('ok', '200', 'OK') 
    if not status:
        print "ERROR: Not able to create \"%s\" at Todoist.com" % project_name
    elif status[1] == 200:
        print "\"%s\" is created at Todoist.com" % project_name

    # Add project to project_file
    project_dict = status[0]
    config = ConfigParser.RawConfigParser()
    config.add_section(str(project_dict['id'])) # configparser does not accept int as section name
    config.set(str(project_dict['id']), 'id', project_dict['id'])
    config.set(str(project_dict['id']), 'name', project_dict['name'])
    config.set(str(project_dict['id']), 'user_id', project_dict['user_id'])
    config.set(str(project_dict['id']), 'cache_count', project_dict['cache_count'])
    config.set(str(project_dict['id']), 'color', project_dict['color'])
    config.set(str(project_dict['id']), 'indent', project_dict['indent'])
    config.set(str(project_dict['id']), 'item_order', project_dict['item_order'])
    config.set(str(project_dict['id']), 'collapsed', project_dict['collapsed'])
    with open(project_file, 'ab') as configfile:
        config.write(configfile)



def save_projects():
    if os.path.exists(project_file):
        os.remove(project_file)

    conf = GetUserInfo()
    token = conf.api_token
    json_projects, status, response = backend.project.get_info(token)

    config = ConfigParser.RawConfigParser()
    for project_dict in json_projects:
        safe_str = project_dict['name'].encode('ascii', 'ignore')
        config.add_section(str(project_dict['id'])) # configparser does not accept int as section name
        config.set(str(project_dict['id']), 'id', project_dict['id'])
        config.set(str(project_dict['id']), 'name', safe_str)
        config.set(str(project_dict['id']), 'user_id', project_dict['user_id'])
        config.set(str(project_dict['id']), 'cache_count', project_dict['cache_count'])
        config.set(str(project_dict['id']), 'color', project_dict['color'])
        config.set(str(project_dict['id']), 'indent', project_dict['indent'])
        config.set(str(project_dict['id']), 'item_order', project_dict['item_order'])
        config.set(str(project_dict['id']), 'collapsed', project_dict['collapsed'])

    with open(project_file, 'wb') as configfile:
        config.write(configfile)

    print "All projects are downloaded and stored to %s" % project_file

def delete_project(args):
    conf = GetUserInfo()
    token = conf.api_token
    config = ConfigParser.RawConfigParser()
    config.read(project_file)

    #TODO: find a more elegant solution, I hate nested for loops
    for id_name in config.sections():
        project_name = config.get(id_name, 'name')
        item_order = config.get(id_name, 'item_order')

        for project in args:
            deleted = False
            if project.isdigit():
                if item_order == project:
                    print "removed section: %s" % id_name
                    config.remove_section(id_name) # Remove also from project_file
                    status = backend.project.delete_project(token, id_name)
                    deleted = project_name
            else:
                if project_name == project:
                    config.remove_section(id_name) # Remove also from project_file
                    status = backend.project.delete_project(token, id_name)
                    deleted = project_name

            # status has two types, the if/else condition must start with status
            # status=False , status = ('ok', '200', 'OK') 
            if deleted:
                if not status:
                    print "ERROR: Not able to delete \"%s\" from Todoist.com" % deleted
                elif status[1] == 200:
                    print "\"%s\" is deleted from Todoist.com" % deleted

    # we have removed sections, thus write changes
    with open(project_file, 'wb') as configfile:
        config.write(configfile)

def rename_project(projects):
    conf = GetUserInfo()
    token = conf.api_token
    config = ConfigParser.RawConfigParser()
    config.read(project_file)

    # Seperate via ",", however that might be changed
    projects = " ".join(projects).split(",")

    #TODO: find a more elegant solution, I hate nested for loops
    for id_name in config.sections():
        section_name = config.get(id_name, 'name')

        if section_name == projects[0].strip():
            config.remove_section(id_name) # Remove also from project_file
            status = backend.project.update_project(token, id_name, projects[1].strip())

    if not status:
        print "ERROR: Not able to rename \"%s\" at Todoist.com" % projects[0].strip()
    elif status[1] == 200:
        print "\"%s\" is renamed to \"%s\"" % (projects[0].strip(), projects[1].strip())

    # Add project to project_file
    project_dict = status[0]
    config = ConfigParser.RawConfigParser()
    config.add_section(str(project_dict['id'])) # configparser does not accept int as section name
    config.set(str(project_dict['id']), 'id', project_dict['id'])
    config.set(str(project_dict['id']), 'name', project_dict['name'])
    config.set(str(project_dict['id']), 'user_id', project_dict['user_id'])
    config.set(str(project_dict['id']), 'cache_count', project_dict['cache_count'])
    config.set(str(project_dict['id']), 'color', project_dict['color'])
    config.set(str(project_dict['id']), 'indent', project_dict['indent'])
    config.set(str(project_dict['id']), 'item_order', project_dict['item_order'])
    config.set(str(project_dict['id']), 'collapsed', project_dict['collapsed'])
    with open(project_file, 'ab') as configfile:
        config.write(configfile)


def argument():
    parser = argparse.ArgumentParser(description='CLI for Todoist',
                                     prog='cit',
                                     usage='%(prog)s [options]')

    parser.add_argument('-v', '--version',
                         action='version',
                         version='%(prog)s 0.0.1')

    #TODO feature realese
#    parser.add_argument('--user-info',
#                        action='store_true',
#                        dest='get_user_info',
#                        default=False,
#                        help="Print user information")

    subparsers = parser.add_subparsers(help='Commands')
    parser_add = subparsers.add_parser('add', help='Add new tasks or projects')
    parser_add.add_argument('add',
                            nargs='*',
                            help="Add task to project")
    parser_add.add_argument('-p', '--project',
                            nargs='*',
                            dest='add_project',
                            action='store',
                            help="Add project")


    parser_del = subparsers.add_parser('rm', help='Remove tasks and projects')
    parser_del.add_argument('rm', nargs='*')
    parser_del.add_argument('-p', '--delete-project',
                            nargs='*',
                            action='store',
                            help="Delete project")

    parser_list = subparsers.add_parser('ls', help='List all uncompleted tasks')
    parser_list.add_argument('ls', nargs='*')

    parser_projects = subparsers.add_parser('projects', help='List all available projects,')
    parser_projects.add_argument('projects', nargs='*')

    parser_save = subparsers.add_parser('save', help='Store User informations, tasks, projects')
    parser_save.add_argument('save', nargs='*')
    parser_save.add_argument('-a',
                        action='store_true',
                        default=False,
                        dest='save_all',
                        help="Download and store all tasks,projects and user info.")
    parser_save.add_argument('-i',
                        nargs=2,
                        action='store',
                        metavar=('username', 'password'),
                        dest='save_info',
                        help="Download and store user informations to \"%s\"" % conf_file)

    parser_update = subparsers.add_parser('up', help='Update tasks and projects')
    parser_update.add_argument('up', nargs='*')
    parser_update.add_argument('-p', '--rename-project',
                        nargs='*',
                        action='store',
                        help="Rename project")




    # We have to set them all to false, otherwise optional arguments are not
    # passed to the args() namespace
    parser.set_defaults(add=None,
                        add_project=None,
                        ls=None,
                        projects=None,
                        rm=None,
                        up=None,
                        save=None,
                        delete_project=None,
                        delete_items=None,
                        save_all=None,
                        save_info=None,
                        rename_project=None)


    return parser.parse_args()

class GetUserInfo():
    def __init__(self):

        config = ConfigParser.RawConfigParser()
        config.read(conf_file)
        self.username = config.get('user_info', 'username')
        self.password = config.get('user_info', 'password')
        self.full_name = config.get('user_info', 'full_name')
        self.unique_id = config.get('user_info', 'id')
        self.api_token = config.get('user_info', 'api_token')
        self.start_page = config.get('user_info', 'start_page')

        self.timezone = config.get('user_info', 'timezone')
        self.tz_offset = config.get('user_info', 'tz_offset')
        self.time_format = config.get('user_info', 'time_format')

        self.date_format = config.get('user_info', 'date_format')
        self.sort_order = config.get('user_info', 'sort_order')
        #TODO: find a way to check for premium user
        #        self.notifo = config.get('user_info', 'notifo')
        #        self.premium_until = config.get('user_info', 'premium_until')
        #        self.default_reminder = config.get('user_info', 'default_reminder')


if __name__ == "__main__":
    args = argument()
    sys.exit(main(args))


