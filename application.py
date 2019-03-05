# usr/bin/python -tt
from catalog_database_setup import Base, Catalog, CatalogItem, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, flash
# New imports for login step
from flask import session as login_session
import random
import string

# Imports for gconnect step
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


engine = create_engine('sqlite:///catalogitems.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "CatalogItemsApp"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
        return response

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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''Current user
                              is already connected.'''), 200)
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
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists in the database, if not,
    # persists the user in the database
    user_id = getUserID(data['email'])
    print("***************** USER ID {}").format(user_id)
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
              -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = '''https://accounts.google.com/o/oauth2/
             revoke?token=%s''' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if (result['status'] == '200') or ('username' in login_session):
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    print("********* {} ************").format(user_id)
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as err:
        print('User not found: %s\nError: %s' % (query, str(err)))
        return None


# JSON APIs to view Catalog Information
@app.route('/catalog/<int:catalog_id>/item/JSON')
def allCatalogItemsJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(
        catalog_id=catalog_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/JSON')
def catalogItemJSON(catalog_id, item_id):
    Item = session.query(CatalogItem).filter_by(id=item_id).one()
    return jsonify(Item=Item.serialize)


@app.route('/catalog/JSON')
def catalogsJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(restaurants=[c.serialize for c in catalogs])


# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    print("LOGIN SESSION:************ {}").format(login_session)
    catalogs = session.query(Catalog)
    items = session.query(CatalogItem)
    if 'username' not in login_session:
        return render_template('public_catalog.html', catalogs=catalogs,
                               items=items)
    else:
        return render_template('catalog.html', catalogs=catalogs, items=items)


# Show all items for the selected category
@app.route('/catalog/<int:catalog_id>/items')
def showCatalogItems(catalog_id):
    catalogs = session.query(Catalog)
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(catalog_id=catalog.id)
    return render_template('items_for_catalog.html', catalogs=catalogs,
                           catalog=catalog, items=items, catalog_id=catalog_id)


# Show item description for the selected item
@app.route('/catalog/<int:catalog_id>/item/<int:item_id>')
def showCatalogItemDescription(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(CatalogItem).filter_by(
        catalog_id=catalog.id).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    print("show login session: {} and user is= {}".format(
        login_session, creator.id))
    if ('username' not in login_session or
       creator.id != login_session['user_id']):
        return render_template('public_item_desc.html', item=item)
    else:
        return render_template('item_desc.html', item=item)


# Edit the selected item
@app.route('/catalog/item/new', methods=['GET', 'POST'])
def addNewCatalogItem():
    if 'username' not in login_session:
        return redirect('/login')
    catalogs = session.query(Catalog)

    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'],
                              description=request.form['description'],
                              catalog_id=request.form['catalog_name'],
                              user_id=getUserID(login_session['email']))
        session.add(newItem)
        session.commit()
        flash('New Catalog %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showCatalog'))
    else:
        return render_template('add_new_item.html', catalogs=catalogs)


# Edit the selected item
@app.route('/catalog/<int:item_id>/edit', methods=['GET', 'POST'])
def editCatalogItem(item_id):
    catalogs = session.query(Catalog)
    editedItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return '''<script>function myFunction() {alert('You are not
                authorized to edit this Catalog item,. Please create
                your own Catalog item in order to edit.');}</script>
                <body onload='myFunction()''>'''

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['catalog_name']:
            editedItem.catalog_id = request.form['catalog_name']
        session.add(editedItem)
        session.commit()
        flash('Catalog Item Successfully Edited')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('edit_item.html',
                               item=editedItem, catalogs=catalogs)


# Delete the selected item
@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCatalogItem(item_id):
    itemToDelete = session.query(CatalogItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        return '''<script>function myFunction() {alert('You are not
               authorized to delete this Catalog item,. Please create
               your own Catalog item in order to delete.');}</script>
               <body onload='myFunction()''>'''

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Catalog Item Successfully Deleted')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('delete_catalog_item.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
