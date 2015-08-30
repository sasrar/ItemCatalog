# Item Catalog App


## Running the Item Catalog App

Open command prompt or Git Bash prompt.

Type **ls** to ensure that you are inside the directory that contains project.py, database_setup.py, and two directories named 'templates' and 'static'

Now type **python database_setup.py** to initialize the database.

Type **python lotsofmenus.py** to populate the database with categories and items. (Optional)

Type **python project.py** to run the Flask web server. In your browser visit **http://localhost:5000** to view the Item Catalog app.  You should be able to view, add, edit, and delete items and categories.
