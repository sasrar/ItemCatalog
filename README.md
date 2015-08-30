# Item Catalog App

## Contents
**Introduction**
**Requirements**
**Running this app**


## Introduction
The Item Catalog app displays a list of items within a variety of categories. It provides a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Requirements
* Python (https://www.python.org/downloads/)
* SqlAlchemy (http://www.sqlalchemy.org/download.html)
* Flask (http://flask.pocoo.org/)
* OAuth2Client (https://github.com/google/oauth2client)

## Running the Item Catalog App

Open command prompt or Git Bash prompt.

Type **ls** to ensure that you are inside the directory that contains project.py, database_setup.py, and two directories named 'templates' and 'static'

Now type **python database_setup.py** to initialize the database.

Type **python lotsofmenus.py** to populate the database with categories and items. (Optional)

Type **python project.py** to run the Flask web server. In your browser visit **http://localhost:5000** to view the Item Catalog app.  You should be able to view, add, edit, and delete items and categories.
