from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
  open('client_secrets.json', 'r').read())['web']['client_id']

#Connect to Database and create database session
engine = create_engine('sqlite:///catalogItems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html")

#JSON APIs to view Restaurant Information
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(Menu_Item = Menu_Item.serialize)

@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants= [r.serialize for r in restaurants])


#Show all categories
@app.route('/')
@app.route('/catalog/')
@app.route('/catalog/<category>/')
@app.route('/catalog/<category>/items/')
def showCatalog(category=""):
  categories = session.query(Category).order_by(asc(Category.name))
  if category == "":
    category = categories.first()
  else:
    category = session.query(Category).filter_by(name = category).one()
  items = session.query(Item).filter_by(category_id = category.id).all()
  
  if 'username' not in login_session:
    return render_template('publicCategories.html', categories = categories, items = items, category_name = category.name)
  else:
    return render_template('categories.html', categories = categories, items = items, category_name = category.name)


#Create a new item
@app.route('/catalog/<category>/items/new/',methods=['GET','POST'])
def newItem(category):
  return 'route works!'
  
  if 'username' not in login_session:
    return redirect(url_for('showLogin'))

  category = session.query(Category).filter_by(name = category).one()
  if request.method == 'POST':
      newItem = Item(name = request.form['name'], description = request.form['description'], category_id = category.id, 
        user_id=login_session['user_id'])
      session.add(newItem)
      session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('showCatalog', category = category.name))
  else:
      return render_template('newItem.html', category = category)

#Show an item
@app.route('/catalog/<category>/<item>/',methods=['GET','POST'])
def showItem(category, item):
  return 'route works!'
  
  category = session.query(Category).filter_by(name = category).one()
  item = session.query(Item).filter_by(name = item).one()

  if 'username' not in login_session:
    return render_template('publicItem.html', category = category, item = item)
  else:
    return render_template('item.html', category = category, item = item)

#Edit an item
@app.route('/catalog/<category>/<item>/edit/', methods=['GET','POST'])
def editItem(category, item):
  return 'route works!'
  if 'username' not in login_session:
    return redirect(url_for('showLogin'))

  editedItem = session.query(Item).filter_by(name = item).one()
  category = session.query(Category).filter_by(name = category).one()
  if request.method == 'POST':
    if request.form['name']:
        editedItem.name = request.form['name']
    if request.form['description']:
        editedItem.description = request.form['description']
    if request.form['price']:
        editedItem.price = request.form['price']
    if request.form['course']:
        editedItem.course = request.form['course']
    session.add(editedItem)
    session.commit() 
    flash('Menu Item Successfully Edited')
    return redirect(url_for('showItem', category = category.name, item = item.name))
  else:
    return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


#Delete an item
@app.route('/catalog/<category>/<item>/delete/', methods=['GET','POST'])
def deleteItem(category, item):
  return 'route works!'
  if 'username' not in login_session:
    return redirect(url_for('showLogin'))

  category = session.query(Category).filter_by(name = category).one()
  itemToDelete = session.query(Item).filter_by(name = item).one() 
  if request.method == 'POST':
    session.delete(itemToDelete)
    session.commit()
    flash('Menu Item Successfully Deleted')
    return redirect(url_for('showMenu', restaurant_id = restaurant_id))
  else:
    return render_template('deleteMenuItem.html', item = itemToDelete)

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

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
  # Only disconnect a connected user.
  credentials = login_session.get('credentials')
  if credentials is None:
      response = make_response(
          json.dumps('Current user not connected.'), 401)
      response.headers['Content-Type'] = 'application/json'
      return response

  access_token = credentials.access_token
  url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
  h = httplib2.Http()
  result = h.request(url, 'GET')[0]

  if result['status'] == '200':
      # Reset the user's sesson.
      del login_session['credentials']
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

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
  if request.args.get['state'] != login_session['state']:
    response = make_response(json.dumps('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  access_token = request.data

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
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
  app.run(host = '0.0.0.0', port = 5000)
