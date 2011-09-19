cit - a cli for todoist.com
===========================

Overview
--------
cit is a simple CLI(command line interface) for the web todo list application
todoist.com.

The name is abbreviated from cli and todist. It will designed to be used easily
and should have the same feeling like using Todoist.com.

Part of the backend is based on Nicholas Schiefer's pydoist
(https://github.com/nickname/pydoist)

It's not the same codebase, you will encounter a whole different set of
functions. I will and have change the code for my own style(Just answered why I
didn't fork it)


Features
--------
A snapshot will be released with the version number 0.1 as soon as I get usable
code.  As for now, the development branch is able to

* Add new tasks
* Add new projects
* Delete tasks
* Delete projects
* Rename currently projects
* List projects
* List tasks in each project ( can accept multiple projects as option)
* Download all your projects and tasks


Requires
--------

* Python 2.7
* Account on Todoist.com


Usage
_____

You can list all options via the help option::

    cit -h

Assuming that you've already have an account on Todoist.com. For the first
setup just run::

    cit save -i username password
    cit save -a

This will download all tasks,projects and user information in your home directory.
But be cautios as your password and api token is stored in ~/.citrc in plaintext.
To sync cit with todoist.com simple just enter(you might need this if you have
changes in the website ::

    cit save -a

To list your projects::

    cit ls

Every projects has a number left aligned. This shows the order of the projects.
**cit** makes it easy to list your task. Just append the number or the project
name to the *ls* command::

    cit ls 1
    cit ls Project


Adding task is also very simple. Just write it down and append the project name
or order number at the end. **cit** will automatically detect your task. You
don't have to use quotes or anything like that (Use quotes only for items that
contains special characters.). You can also append the order number of a
project if you know it::

    cit add This is a task +Project
    cit add This is a task +1

To add a project with the name *Work*::

    cit add -p Work

**cit** is able to delete multiple tasks. Once the task in a project is listed,
you can easily delete task with their associated order numbers. The command
below will delete task with the order number 1 that's belong to the project
*foo*. Again, you can use the project with the project's order number too::

    cit rm 1 +foo
    cit rm 1 +1

To remove a project wit the name *Freelance*, just write the name or the order
number of this project (assume it has 3)::

    cit rm -p Freelance
    cit rm -p 3




















