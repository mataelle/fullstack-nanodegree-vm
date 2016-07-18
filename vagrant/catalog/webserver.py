from flask import Flask, render_template, redirect, request, url_for, jsonify, make_response, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User
import json, httplib2
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import requests


engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
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
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions

def createUser(login_session):
    user = User(name = login_session['username'],
                   email=login_session['email'])
    session.add(user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUser():
    if 'username' not in login_session:
      return None
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    del login_session['gplus_id']
    del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['user_id']
    del login_session['provider']
    return redirect(url_for('MainHandler'))

#### json endpoints

@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    return jsonify(items=[i.serialize for i in category.items])

@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(catalog=[c.serialize for c in categories])

#### handlers

@app.route('/category/<int:category_id>')
def CategoryHandler(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    return render_template('category.html', category=category, user=getUser())

@app.route('/category/<int:category_id>/item/<int:item_id>')
def ItemHandler(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('item.html', item=item, user=getUser())

@app.route('/category/<int:category_id>/item/new', methods = ['GET', 'POST'])
def NewItemHandler(category_id):
    if request.method == 'GET':
        user = getUser()
        if not user:
          return render_template('error_forbidden.html')
        category = session.query(Category).filter_by(id = category_id).one()
        return render_template('item_new.html',
                               category = category,
                               user=getUser())
    else:
        user = getUser()
        if not user:
          return render_template('error_forbidden.html')
        name = request.form.get('item_name', None)
        description = request.form.get('description', None)
        category = session.query(Category).filter_by(id = category_id).one()
        if not name or not description:
           return render_template('item_new.html',
                                  category = category,
                                  name = name,
                                  description = description,
                                  err_msg = True,
                                  user=getUser())
        item = Item(name = name, description = description, category=category, user=getUser())
        session.add(item)
        session.commit()
        return redirect(url_for('ItemHandler', category_id = category_id, item_id = item.id))

@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def EditItemHandler(category_id, item_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id = category_id).one()
        item = session.query(Item).filter_by(id = item_id).one()
        user = getUser()
        if not user or item.user_id != user.id:
          return render_template('error_forbidden.html')
        return render_template('item_edit.html',
                               item_id = item_id,
                               category = category,
                               name = item.name,
                               description = item.description,
                               user=getUser())
    else:
        name = request.form.get('item_name', None)
        description = request.form.get('description', None)
        if not name or not description:
           return render_template('item_edit.html',
                                  item_id = item_id,
                                  name = name,
                                  description = description,
                                  err_msg = True,
                                  user=getUser())
        category = session.query(Category).filter_by(id = category_id).one()
        item = session.query(Item).filter_by(id = item_id).one()
        user = getUser()
        if not user or item.user_id != user.id:
          return render_template('error_forbidden.html')
        item.name = name
        item.description = description
        session.add(item)
        session.commit()
        return render_template('item.html',
                                category=category,
                                item=item,
                                user=getUser())

@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def DeleteItemHandler(category_id, item_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id = category_id).one()
        item = session.query(Item).filter_by(id = item_id).one()
        user = getUser()
        if not user or item.user_id != user.id:
          return render_template('error_forbidden.html')
        return render_template('item_delete.html',
                                category=category,
                                item_id = item_id,
                                user=getUser())
    else:
        category = session.query(Category).filter_by(id = category_id).one()
        item = session.query(Item).filter_by(id = item_id).one()
        user = getUser()
        if not user or item.user_id != user.id:
          return render_template('error_forbidden.html')
        session.delete(item)
        session.commit()
        return redirect(url_for('CategoryHandler', category_id = category_id))

@app.route('/category')
@app.route('/')
def MainHandler():
    categories = session.query(Category).all()
    # latest_items = session.query(Item).order_by('created').limit(10)
    return render_template('front.html',
                            categories=categories,
                            user=getUser())

if __name__ == "__main__":
    app.secret_key = 'big big secret'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)