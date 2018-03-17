from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import SmartPhone, Base, PhoneModel, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Smartphone Catalog Application"

engine = create_engine('sqlite:///smartphonemodelcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create anti-forgery state token for login_session
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Third party authentication using google-signin : establishing connection
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Gathers data from Google Sign In API and places it inside a session variable.
    """
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
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.\
                                            '), 200)
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
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


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


# Third party authentication using google-signin : # Disconnect
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not \
                                            connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given \
                                            user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Third party authentication using facebook signin : establishing connection
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
    Gathers data from Facebook Sign In API and places it inside a session variable.
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (  # noqa
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token
        exchange we have to split the token first on commas and select
        the first index which gives us the key : value for the server
        access token then we split it on colons to pull out the actual
        token value and replace the remaining quotes with nothing so that
        it can be used directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output


# Third party authentication using facebook signin : # Disconnect
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)   # noqa
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showSmartphones'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showSmartphones'))


# JSON API to view smartphone catalog information
@app.route('/smartphones/JSON')
def showRestaurantsJSON():
    smartphones = session.query(SmartPhone).all()
    return jsonify(SmartPhones=[phone.serialize for phone in smartphones])


@app.route('/smartphone/<int:smartPhone_id>/model/JSON')
def showModelsJSON(smartPhone_id):
    smart_phone = session.query(SmartPhone).filter_by(id=smartPhone_id).one()
    phone_models = session.query(PhoneModel).filter_by(smartPhone_id=smartPhone_id).all()  # noqa
    return jsonify(phoneModels=[i.serialize for i in phone_models])


@app.route('/smartphone/<int:smartPhone_id>/model/<int:model_id>/JSON')
def modelJSON(smartPhone_id, model_id):
    model = session.query(PhoneModel).filter_by(id=model_id).one()
    return jsonify(Model=[model.serialize])


# Show the list of smartphonemodels
@app.route('/')
@app.route('/smartphones')
def showSmartphones():
    smartPhones = session.query(SmartPhone).order_by(asc(SmartPhone.name))
    if 'username' not in login_session:
        return render_template('publicsmartphones.html',
                               smartPhones=smartPhones)
    else:
        return render_template('smartphones.html', smartPhones=smartPhones)


# Create a new category of smartphone models
@app.route('/smartphones/new', methods=['GET', 'POST'])
def newSmartphone():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == "POST":
        newCategory = SmartPhone(name=request.form['name'],
                                 user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('New Category of SmartPhone has been added!')
        return redirect(url_for('showSmartphones'))
    else:
        return render_template('newsmartphone.html')


# Edit a smartphone models
@app.route('/smartphone/<int:smartPhone_id>/edit', methods=['GET', 'POST'])
def editSmartphone(smartPhone_id):
    editPhone = session.query(SmartPhone).filter_by(id=smartPhone_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editPhone.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized "\
               "to edit this model!');}</script><body onload='myFunction()'>"
    if request.method == "POST":
        if request.form['name']:
            editPhone.name = request.form['name']
        session.add(editPhone)
        session.commit()
        flash('A Category of SmartPhone has been edited!')
        return redirect(url_for('showSmartphones'))
    else:
        return render_template('editsmartphone.html', smartPhone=editPhone)


# Delete a smartphone models
@app.route('/smartphone/<int:smartPhone_id>/delete', methods=['GET', 'POST'])
def deleteSmartphone(smartPhone_id):
    deletePhone = session.query(SmartPhone).filter_by(id=smartPhone_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletePhone.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
            "to delete this model!');}</script><body onload='myFunction()'>"
    if request.method == "POST":
        session.delete(deletePhone)
        session.commit()
        flash('A Category of SmartPhone has been deleted!')
        return redirect(url_for('showSmartphones'))
    else:
        return render_template('deletesmartphone.html', smartPhone=deletePhone)


# Show the list of models from a specific category
@app.route('/smartphones/<int:smartPhone_id>')
@app.route('/smartphones/<int:smartPhone_id>/model')
def showModels(smartPhone_id):
    smartPhone = session.query(SmartPhone).filter_by(id=smartPhone_id).one()
    creator = getUserInfo(smartPhone.user_id)
    model = session.query(PhoneModel).filter_by(
        smartPhone_id=smartPhone_id).all()
    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        return render_template('publicModel.html',
                               model=model,
                               smartPhone=smartPhone,
                               creator=creator)
    else:
        return render_template('Model.html', model=model,
                               smartPhone=smartPhone, creator=creator)


# Create a new models to a specific category of smartphones
@app.route('/smartphones/<int:smartPhone_id>/model/new',
           methods=['GET', 'POST'])
def newModel(smartPhone_id):
    if 'username' not in login_session:
        return redirect('/login')
    smartPhone = session.query(SmartPhone).filter_by(id=smartPhone_id).one()
    if smartPhone.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
             "to add new model category!');}"\
             "</script><body onload='myFunction()'>"
    if request.method == "POST":
        newPhonemodel = PhoneModel(name=request.form['name'],
                                   description=request.form['description'],
                                   price=request.form['price'],
                                   os=request.form['os'],
                                   memory=request.form['memory'])
        newPhonemodel.smartPhone_id = smartPhone_id
        session.add(newPhonemodel)
        session.commit()
        flash('New model has been added to this smartphone category')
        return redirect(url_for('showModels', smartPhone_id=smartPhone_id))
    else:
        return render_template(
            'newphonemodel.html', smartPhone_id=smartPhone_id)


# Edit a models in the list of smartphones from a specific category
@app.route('/smartphones/<int:smartPhone_id>/model/<int:model_id>/edit',
           methods=['GET', 'POST'])
def editModel(smartPhone_id, model_id):
    if 'username' not in login_session:
        return redirect('/login')
    editPhonemodel = session.query(PhoneModel).filter_by(id=model_id).one()
    if editPhonemodel.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
               "to edit model in this category!');}"\
               "</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name'] == "":
            editPhonemodel.name = editPhonemodel.name
        else:
            editPhonemodel.name = request.form['name']

        if request.form['description'] == "":
            editPhonemodel.description = editPhonemodel.description
        else:
            editPhonemodel.description = request.form['description']

        if request.form['price'] == "":
            editPhonemodel.price = editPhonemodel.price
        else:
            editPhonemodel.price = request.form['price']

        if request.form['os'] == "":
            editPhonemodel.os = editPhonemodel.os
        else:
            editPhonemodel.os = request.form['os']

        if request.form['memory'] == "":
            editPhonemodel.memory = editPhonemodel.memory
        else:
            editPhonemodel.memory = request.form['memory']
        session.add(editPhonemodel)
        session.commit()
        flash('A model in this smartphone category has been edited!')
        return redirect(url_for('showModels', smartPhone_id=smartPhone_id,
                        model_id=model_id))
    else:
        return render_template('editphonemodel.html',
                               smartPhone_id=smartPhone_id,
                               model_id=model_id,
                               editPhonemodel=editPhonemodel)


# Delete a models in the list of smartphones from a specific category
@app.route('/smartphones/<int:smartPhone_id>/model/<int:model_id>/delete',
           methods=['GET', 'POST'])
def deleteModel(smartPhone_id, model_id):
    if 'username' not in login_session:
        return redirect('/login')
    smartPhone = session.query(SmartPhone).filter_by(id=smartPhone_id).one()
    deletePhonemodel = session.query(PhoneModel).filter_by(id=model_id).one()
    if deletePhonemodel.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
               "to delete model from this category!');}"\
               "</script><body onload='myFunction()'>"
    if request.method == "POST":
        session.delete(deletePhonemodel)
        session.commit
        flash('A model in this smartphone category has been delete!')
        return redirect(url_for('showModels', smartPhone_id=smartPhone_id))
    else:
        return render_template('deletephonemodel.html',
                               smartPhone_id=smartPhone_id,
                               model_id=model_id,
                               deletePhonemodel=deletePhonemodel)


# function to avoid CSS cache
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
