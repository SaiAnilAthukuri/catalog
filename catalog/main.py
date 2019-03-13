from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mobile_setup import Base, MobileCompanyName, MobileName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///mobiles.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Mobiles Store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
mbs_cat = session.query(MobileCompanyName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    mbs_cat = session.query(MobileCompanyName).all()
    mbes = session.query(MobileName).all()
    return render_template('login.html',
                           STATE=state, mbs_cat=mbs_cat, mbes=mbes)
    # return render_template('myhome.html', STATE=state
    # mbs_cat=mbs_cat,mbes=mbes)


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
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
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
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
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
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
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
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

#
# Home


@app.route('/')
@app.route('/home')
def home():
    mbs_cat = session.query(MobileCompanyName).all()
    return render_template('myhome.html', mbs_cat=mbs_cat)

#
# Mobile Category for admins


@app.route('/MobileStore')
def MobileStore():
    try:
        if login_session['username']:
            name = login_session['username']
            mbs_cat = session.query(MobileCompanyName).all()
            mbs = session.query(MobileCompanyName).all()
            mbes = session.query(MobileName).all()
            return render_template('myhome.html', mbs_cat=mbs_cat,
                                   mbs=mbs, mbes=mbes, uname=name)
    except:
        return redirect(url_for('showLogin'))

#
# Showing mobiles based on mobile category


@app.route('/MobileStore/<int:mid>/AllCompanys')
def showMobiles(mid):
    mbs_cat = session.query(MobileCompanyName).all()
    mbs = session.query(MobileCompanyName).filter_by(id=mid).one()
    mbes = session.query(MobileName).filter_by(mobilecompanynameid=mid).all()
    try:
        if login_session['username']:
            return render_template('showMobiles.html', mbs_cat=mbs_cat,
                                   mbs=mbs, mbes=mbes,
                                   uname=login_session['username'])
    except:
        return render_template('showMobiles.html',
                               mbs_cat=mbs_cat, mbs=mbs, mbes=mbes)

#
# Add New Mobile


@app.route('/MobileStore/addMobileCompany', methods=['POST', 'GET'])
def addMobileCompany(): 
    if request.method == 'POST':
        company = MobileCompanyName(
            name=request.form['name'],
            user_id=login_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('MobileStore'))
    else:
        return render_template('addMobileCompany.html', mbs_cat=mbs_cat)

#
# Edit Mobile Category


@app.route('/MobileStore/<int:mid>/edit', methods=['POST', 'GET'])
def editMobileCategory(mid):
    editedMobile = session.query(MobileCompanyName).filter_by(id=mid).one()
    creator = getUserInfo(editedMobile.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Mobile Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('MobileStore'))
    if request.method == "POST":
        if request.form['name']:
            editedMobile.name = request.form['name']
        session.add(editedMobile)
        session.commit()
        flash("Mobile Category Edited Successfully")
        return redirect(url_for('MobileStore'))
    else:
        # mbs_cat is global variable we can them in entire application
        return render_template('editMobileCategory.html',
                               m=editedMobile, mbs_cat=mbs_cat)

######
# Delete Mobile Category


@app.route('/MobileStore/<int:mid>/delete', methods=['POST', 'GET'])
def deleteMobileCategory(mid):
    m = session.query(MobileCompanyName).filter_by(id=mid).one()
    creator = getUserInfo(m.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Mobile Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('MobileStore'))
    if request.method == "POST":
        session.delete(m)
        session.commit()
        flash("Mobile Category Deleted Successfully")
        return redirect(url_for('MobileStore'))
    else:
        return render_template(
            'deleteMobileCategory.html', m=m, mbs_cat=mbs_cat)

######
# Add New Mobile Name Details


@app.route('/MobileStore/addCompany/addMobileDetails/<string:mname>/add',
           methods=['GET', 'POST'])
def addMobileDetails(mname):
    mbs = session.query(MobileCompanyName).filter_by(name=mname).one()
    # See if the logged in user is not the owner of mobile
    creator = getUserInfo(mbs.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new mobile Details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showMobiles', mid=mbs.id))
    if request.method == 'POST':
        modelname = request.form['modelname']
        processor = request.form['processor']
        ram = request.form['ram']
        rom = request.form['rom']
        price = request.form['price']
        screensize = request.form['screensize']
        rating = request.form['rating']
        mobiledetails = MobileName(
            modelname=modelname, processor=processor,
            ram=ram, rom=rom,
            price=price, screensize=screensize,
            rating=rating,
            date=datetime.datetime.now(),
            mobilecompanynameid=mbs.id,
            user_id=login_session['user_id'])
        session.add(mobiledetails)
        session.commit()
        return redirect(url_for('showMobiles', mid=mbs.id))
    else:
        return render_template('addMobileDetails.html',
                               mname=mbs.name, mbs_cat=mbs_cat)

######
# Edit Mobile details


@app.route('/MobileStore/<int:mid>/<string:mename>/edit',
           methods=['GET', 'POST'])
def editMobile(mid, mename):
    m = session.query(MobileCompanyName).filter_by(id=mid).one()
    mobiledetails = session.query(MobileName).filter_by(modelname=mename).one()
    # See if the logged in user is not the owner of Mobile
    creator = getUserInfo(m.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this mobile edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showMobiles', mid=m.id))
    # POST methods
    if request.method == 'POST':
        mobiledetails.modelname = request.form['modelname']
        mobiledetails.processor = request.form['processor']
        mobiledetails.ram = request.form['ram']
        mobiledetails.rom = request.form['rom']
        mobiledetails.price = request.form['price']
        mobiledetails.screensize = request.form['screensize']
        mobiledetails.rating = request.form['rating']
        mobiledetails.date = datetime.datetime.now()
        session.add(mobiledetails)
        session.commit()
        flash("Mobile Edited Successfully")
        return redirect(url_for('showMobiles', mid=mid))
    else:
        return render_template('editMobile.html', mid=mid, 
                               mobiledetails=mobiledetails,
                               mbs_cat=mbs_cat)

##
# Delte Mobile Edit


@app.route('/MobileStore/<int:mid>/<string:mename>/delete',
           methods=['GET', 'POST'])
def deleteMobile(mid, mename):
    m = session.query(MobileCompanyName).filter_by(id=mid).one()
    mobiledetails = session.query(MobileName).filter_by(modelname=mename).one()
    # See if the logged in user is not the owner of mobile
    creator = getUserInfo(m.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this mobile edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showMobiles', mid=m.id))
    if request.method == "POST":
        session.delete(mobiledetails)
        session.commit()
        flash("Deleted Mobile Successfully")
        return redirect(url_for('showMobiles', mid=mid))
    else:
        return render_template('deleteMobile.html',
                               mid=mid, mobiledetails=mobiledetails, 
                               mbs_cat=mbs_cat)

####
# Logout from current user


@app.route('/logout')
def Logout():
    access_token = login_session['access_token']
    print ('In g disconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={
                      'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#####
# Json


@app.route('/MobileStore/JSON')
def allMobilesJSON():
    mobilecategories = session.query(MobileCompanyName).all()
    category_dict = [c.serialize for c in mobilecategories]
    for c in range(len(category_dict)):
        mobiles = [i.serialize for i in session.query(
                 MobileName).filter_by(
                     mobilecompanynameid=category_dict[c]["id"]).all()]
        if mobiles:
            category_dict[c]["mobile"] = mobiles
    return jsonify(MobileCompanyName=category_dict)

####


@app.route('/MobileStore/mobileCategories/JSON')
def categoriesJSON():
    mobiles = session.query(MobileCompanyName).all()
    return jsonify(mobileCategories=[c.serialize for c in mobiles])

####


@app.route('/MobileStore/mobiles/JSON')
def itemsJSON():
    items = session.query(MobileName).all()
    return jsonify(mobiles=[i.serialize for i in items])


@app.route('/MobileStore/<path:mobile_name>/mobiles/JSON')
def categoryItemsJSON(mobile_name):
    mobileCategory = session.query(
        MobileCompanyName).filter_by(name=mobile_name).one()
    mobiles = session.query(MobileName).filter_by(
        mobilecompanyname=mobileCategory).all()
    return jsonify(mobileEdtion=[i.serialize for i in mobiles])


@app.route('/MobileStore/<path:mobile_name>/<path:edition_name>/JSON')
def ItemJSON(mobile_name, edition_name):
    mobileCategory = session.query(
        MobileCompanyName).filter_by(name=mobile_name).one()
    mobileEdition = session.query(MobileName).filter_by(
           modelname=edition_name, mobilecompanyname=mobileCategory).one()
    return jsonify(mobileEdition=[mobileEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8888)
