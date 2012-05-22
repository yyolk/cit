cit - a cli for todoist.com
===========================

Overview
--------
cit is a simple CLI(command line interface) for the web todo list application
todoist.com.

The name is abbreviated from cli and todist. It will designed to be used easily
and should have the same feeling like using Todoist.com. The backend is based
on Nicholas Schiefer's pydoist (https://github.com/nickname/pydoist)


Features
--------
A snapshot will be released with the version number 0.1 as soon as I get usable
code.  As for now, the development branch is able to

* Add new tasks
* Add new projects
* Delete tasks
* Delete projects
* Rename currently projects
* List tasks in each project (can accept multiple projects as option)
* List projects

Todo
----

* Store login credentials encrypted
* "Done" should be implemented
* Unicode support
* Support premium features
* Better solution to store data (currently configparser)
* .. add yours


Requires
--------

* Python 2.7
* Account on Todoist.com


Usage
_____

**ASCII ONLY!** Unicode characters are not supported for now. Please be aware of 
this problem before you begin to use.

You can list all options via the help option::

    cit -h

Assuming that you've already have an account on Todoist.com. For the first
setup just run::

    cit save -i username password

This will download all tasks,projects and user information in your home directory.
But be cautios as your password and api token is stored in ~/.citrc in **plaintext**.
For re-download of all your task just run::

    cit save -a

To list all uncompleted items::

    cit ls

You can easily filter your items by project names. It also accepts multiple projects
The command below show only items that belongs to the "work" and "private" project::

    cit ls +work +private

Creating a new task is also very simple. Just write it and append the project
name or order number at the end. (Use quotes only for items that contains
special characters.)::

    cit add This is a task +1
    cit add This is a task +ProjectName

Creating a new project with the name *Work*::

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





















