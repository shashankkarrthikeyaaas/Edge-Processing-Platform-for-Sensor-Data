# Importing API resources
from Gateway import API_Resources as api_res

# Import Flask Module for running a API Server
import flask
from flask import Flask, jsonify, request, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager


# Main Class
class App:
    # Used to create a object that performs all Web Jobs
    def __init__(self):
        # Creates a Flask Object
        self.__app = flask.Flask(__name__)

        self.__app.config['PROPAGATE_EXCEPTIONS'] = True

        # This secret key is used to propagate tokens
        self.__app.secret_key = 'asdfghjkl'

        # Enabling blacklisting of tokens
        self.__app.config['JWT_BLACKLIST_ENABLED'] = True
        self.__app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
        self.__app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

        # Creating an API Object
        self.__api = Api(self.__app)

        # Creating a Object of Resources Class
        self.__res = api_res.Resources()
        self.__jwt = JWTManager(self.__app)

        # Checking if JWT is blacklisted
        @self.__jwt.token_in_blacklist_loader
        def check_if_token_in_blacklist(decrypted_token):
            return decrypted_token['jti'] in self.__res.BLACKLIST

        # Callback for expired token
        @self.__jwt.expired_token_loader
        def expired_token_callback():
            response = jsonify({'status': 401,
                                'message': 'The token has expired',
                                'error': 'token_expired'
                                })
            response.status_code = 401
            return response

        # Callback for Invalid token
        @self.__jwt.invalid_token_loader
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
        @self.__jwt.unauthorized_loader
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
        @self.__jwt.needs_fresh_token_loader
        def token_not_fresh_callback():
            response = jsonify({
                "description": "The token is not fresh.",
                'error': 'fresh_token_required',
                'status': '401'
            })
            response.status_code = 401
            return response

        # Callback for revoked token
        @self.__jwt.revoked_token_loader
        def revoked_token_callback():
            response = jsonify({
                "description": "The token has been revoked.",
                'error': 'token_revoked',
                'status': '401'
            })
            response.status_code = 401
            return response

        # Linking Classes from resources into API
        self.__api.add_resource(self.__res.Welcome, '/welcome')
        self.__api.add_resource(self.__res.Signup, '/signup')
        self.__api.add_resource(self.__res.UserLogin, '/login')
        self.__api.add_resource(self.__res.UserLogout, '/logout')
        self.__api.add_resource(self.__res.KillToken, '/killtoken')
        self.__api.add_resource(self.__res.TokenRefresh, '/refreshtoken')

        self.__api.add_resource(self.__res.Time_Interval_Update, '/update')

        self.__api.add_resource(self.__res.Content, '/content')


    # Function to execute the object
    def run(self, port_in, host_in):
        self.__app.run(port=port_in, host=host_in )
