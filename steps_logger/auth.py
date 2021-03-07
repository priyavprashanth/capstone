from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Response,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from .config import configAuth0
import requests
import urllib3

import json
# Priya - imported abort from flask as have implemented abort function mostly, referred the link https://stackoverflow.com/questions/41768866/what-exactly-does-flask-abort-do
from flask import _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from six.moves.urllib.request import urlopen
from flask_cors import cross_origin

AUTH0_DOMAIN = configAuth0['AUTH0_DOMAIN']  # Priya : added domain
ALGORITHMS = configAuth0['ALGORITHMS']
API_AUDIENCE = configAuth0['API_AUDIENCE']
AUTH0_CALLBACK_URL = 'https://steps-logger.herokuapp.com/memProfile'

'''
Priya Note to the Reviewer: 
1. Have listed out the requirements from the Rubric below as TODO from Rubric.
2. For each of these requirements, have added a comment specifying the details 
of completion of the requirement.
3. In addition, the function get_token_auth_header is written in-line with the 
requirements from the Coffee Shop assignment
4. For the requirement c. take an argument to describe the action - this is completed 
for the enpoint /allUsers defined in main.py. Below are the lines of code for your reference:
@main.route("/allUsers", methods=['GET','POST'])
@requires_auth('get:steps-all')
5. For the requirement d. raise an error if the JWT doesn’t contain the proper action - this is completed
in the function : check_permissions(permission, payload) 

TODO from Rubric:
	1. Project includes a custom @requires_auth decorator that:
		a. get the Authorization header from the request
		b. Decode and verify the JWT using the Auth0 secret
		c. take an argument to describe the action i.e. @require_auth(‘create:drink’)
           Priya Note to the reviewer : This is completed in main.py - please check point 4 in the notes above
            
		d. raise an error if:
			i. the token is expired
			ii. the claims are invalid
			iii. the token is invalid
            iv. the JWT doesn’t contain the proper action 
'''

# Priya note to the reviewer : Below AuthError exception has been used for status codes 400, 401 and 403
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Priya - @TODO : 1. Project includes a custom @requires_auth decorator - DONE
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Retrieves the Authorization header from the request, uses the get_token_auth_header method to get the token
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)

            except:
                abort(401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        # Returns the decorator which passes the decoded payload to the decorated method
        return wrapper
    return requires_auth_decorator


def get_token_auth_header():
    auth_in_header = request.headers.get('Authorization', None)
    #print('auth_in_header value: ', auth_in_header)

    # Raises an AuthError if no header is present
    if not auth_in_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected and was not provided'
        }, 401)

    # Attempts to split bearer and the token
    split_bearer_token = auth_in_header.split(' ')

    # Raises an AuthError if the header is malformed
    # 2 cases, 1. if there is no bearer and token, 2. when token is not prefixed with bearer
    if len(split_bearer_token) != 2:
        raise AuthError({
            'code': 'bearer or token missing',
            'description': 'Authorization header should contain token prefixed with Bearer separated by space'
        }, 401)

    elif split_bearer_token[0].lower() != 'bearer':
        raise AuthError({
            'code': 'bearer prefix not there with token',
            'description': 'Authorization header should contain token prefixed with Bearer separated by space'
        }, 401)

    # Returns the token part of the header
    token = split_bearer_token[1]
    return(token)
# 
# Priya - @TODO : d. raise an error if the JWT doesn’t contain the proper action - Done


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

# Priya - @TODO : b. Decode and verify the JWT using the Auth0 secret - DONE


def verify_decode_jwt(token):
    # Token is verified to be an Auth0 token with key id (kid)
    # verified the token using Auth0 /.well-known/jwks.json
    # Priya - Note to reviewer - When writing the below function, came across many errors, errors were fixed after referring to
    # 1.  https://auth0.com/docs/quickstart/backend/python/01-authorization and made the change. After making the change, it worked.
    # 2. https://community.auth0.com/t/internal-server-error-can-not-convert-none-type-to-str-implicitly-from-apache2-error-log/27517/10 for jwks = json.loads(jsonurl.readline().decode('utf-8'))
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.readline().decode('utf-8'))
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Decodes the payload from the token
    ISSUER = "https://"+AUTH0_DOMAIN+"/"
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            # Returns the decoded payload
            return payload

        # Priya : @TODO : i. Raise an error if token is expired : DONE
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        # Priya @TODO : ii. Raise an error if the claims are invalid - DONE
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        # Priya - @TODO : iii. Raise an error if the token is invalid - DONE
        # Referred the practice code provided from the Chapter Identity and Access Management
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
        _request_ctx_stack.top.current_user = payload

    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


auth = Blueprint('auth', __name__)


@auth.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signupUser():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Checking if user already exists in database
    user = User.query.filter_by(email=email).first()

    print(user)

    # if user already exists then redirect to signup page to try again
    if user:
        flash('Try with another email id, this id is already taken')
        return redirect(url_for('auth.signup'))

    # Create the new user, hash the password before storing in the database.
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    # Adding the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def loggingInUser():
    print(request.headers)
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/memLogin')
@cross_origin(headers=["Content-Type", "Authorization"])
def memLogin():
    link = 'https://prisha.au.auth0.com/authorize?audience=stepsLogger&response_type=token&client_id=qXot7M1Z3VlF5e3cHMg7IAXzDHDNYJdK&redirect_uri=https://steps-logger.herokuapp.com/memProfile'
    return redirect(link)

# Priya Note to the reviewer : Below function was written to automate the task of manually adding the jwt token
# as bearer token in postman under authorization headers


@auth.route('/loginWithToken', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def loginWithToken():
    gen_token = request.form.get('token')
    bearer_token = 'Bearer '+gen_token
    # First just check the permissions and accordingly send them to admin page or the user page.
    try:
        # Getting the payload to  get the permissions.
        payload = verify_decode_jwt(gen_token)
    except:
        abort(401)

    # Check if there are permissions in the payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    permissions = payload['permissions']
    # print('Permission', permission)
    # Priya : get:steps-all is the permission for an admin therefore they are forwarded to the admin page /allUsers
    if ('get:steps-all' in permissions):
        url = 'https://steps-logger.herokuapp.com/allUsers'
        headers = {"Authorization": bearer_token}
        resp = requests.post(url, headers=headers)
        res = Response(resp)
    # Priya : get:steps-detail is the permission for a specific user, he / she is forwarded to user page /user
    elif('get:steps-detail' in permissions):
        url = 'https://steps-logger.herokuapp.com/user'
        headers = {"Authorization": bearer_token}
        resp = requests.post(url, headers=headers)
        res = Response(resp)

    return res


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
