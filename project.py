from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogItems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)

# Show catalog data in json format
@app.route('/catalog.json/')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])

# Show all categories
@app.route('/')
@app.route('/catalog/')
@app.route('/catalog/<category>/')
@app.route('/catalog/<category>/items/')
def showCatalog(category=""):
    categories = session.query(Category).order_by(asc(Category.name))
    if category == "":
        category = categories.first()
    else:
        category = session.query(Category).filter_by(name=category).one()
    items = session.query(Item).filter_by(category_id=category.id).all()

    if 'username' not in login_session:
        return render_template(
            'publicCategories.html',
            categories=categories,
            items=items,
            category_name=category.name)
    else:
        return render_template(
            'categories.html',
            categories=categories,
            items=items,
            category_name=category.name)


# Create a new item
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        category = session.query(Category).filter_by(
            name=request.form['category']).one()

        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category=category,
            user_id=login_session['user_id'])

        session.add(newItem)
        session.commit()
        flash('New %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showCatalog', category=category.name))
    else:
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('newItem.html', categories=categories)

# Show an item
@app.route('/catalog/<category>/<item>/', methods=['GET', 'POST'])
def showItem(category, item):
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(Item).filter_by(name=item).one()

    if 'username' not in login_session:
        return render_template('publicItem.html', category=category, item=item)
    else:
        return render_template('item.html', category=category, item=item)

# Edit an item
@app.route('/catalog/<item>/edit/', methods=['GET', 'POST'])
def editItem(item):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    editedItem = session.query(Item).filter_by(name=item).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            category = session.query(Category).filter_by(
                name=request.form['category']).one()
            editedItem.category = category
        session.add(editedItem)
        session.commit()
        flash('Item %s Successfully Edited' % (editedItem.name))
        return redirect(url_for('showItem', category=category.name,
                                item=editedItem.name))
    else:
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('editItem.html', item=editedItem,
                               categories=categories)


# Delete an item
@app.route('/catalog/<item>/delete/', methods=['GET', 'POST'])
def deleteItem(item):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    itemToDelete = session.query(Item).filter_by(name=item).one()
    category = itemToDelete.category
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item %s Successfully Deleted' % (itemToDelete.name))
        return redirect(url_for('showCatalog', category=category.name))
    else:
        return render_template('deleteItem.html', item=itemToDelete)

# Connect using google+ account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        # Upgrade authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentialsAccessToken = login_session.get('credentialsAccessToken')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentialsAccessToken is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentialsAccessToken'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Disconnect user
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentialsAccessToken = login_session.get('credentialsAccessToken')
    if credentialsAccessToken is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentialsAccessToken
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentialsAccessToken']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# User Helper Functions
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
