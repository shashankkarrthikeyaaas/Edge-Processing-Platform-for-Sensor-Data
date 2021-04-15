from Gateway import API_Resources as api_res

# Import Flask Module for running a API Server
import flask
from flask import Flask, jsonify, request, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager


# Main Class

# Used to create a object that performs all Web Jobs

app = flask.Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

# This secret key is used to propagate tokens
app.secret_key = 'asdfghjkl'

# Enabling blacklisting of tokens
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

# Creating an API Object
api = Api(app)

# Creating a Object of Resources Class
res = api_res.Resources()
jwt = JWTManager(app)

# Checking if JWT is blacklisted
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in res.BLACKLIST

# Callback for expired token
@jwt.expired_token_loader
def expired_token_callback():
    response = jsonify({'status': 401,
                        'message': 'The token has expired',
                        'error': 'token_expired'
                        })
    response.status_code = 401
    return response

# Callback for Invalid token
@jwt.invalid_token_loader
def invalid_token_callback(
        error):  # we have to keep the argument here, since it's passed in by the caller internally
    response = jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token',
        'status': '401'
    })
    response.status_code = 401
    return response

# Callback for Missing token
@jwt.unauthorized_loader
def missing_token_callback(error):
    response = jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required',
        'status': '401'
    })
    response.status_code = 401
    return response

# Callback for Fresh token required
# Not used in this program
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    response = jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required',
        'status': '401'
    })
    response.status_code = 401
    return response

# Callback for revoked token
@jwt.revoked_token_loader
def revoked_token_callback():
    response = jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked',
        'status': '401'
    })
    response.status_code = 401
    return response

# Linking Classes from resources into API
api.add_resource(res.Welcome, '/welcome')
api.add_resource(res.Signup, '/signup')
api.add_resource(res.UserLogin, '/login')
api.add_resource(res.UserLogout, '/logout')
api.add_resource(res.KillToken, '/killtoken')
api.add_resource(res.TokenRefresh, '/refreshtoken')

api.add_resource(res.Time_Interval_Update, '/update')

api.add_resource(res.Content, '/content')
# app.run(port=8080, host='0.0.0.0')
