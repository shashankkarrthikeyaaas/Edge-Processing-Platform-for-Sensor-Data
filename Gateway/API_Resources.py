# Import Database module from Database.py
from Gateway import WEB_Database as db
from Gateway import IOT_Database as iot
# Importing Resource and Parser for flask MOdule
from flask import jsonify,request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
create_refresh_token ,
jwt_refresh_token_required ,
get_jwt_identity,
jwt_required,
get_raw_jwt)

import json

# Import this module to compare passwords in a secured way
from werkzeug.security import safe_str_cmp

# Creating Web Database Object
db_web = db.WEB_Database()
db_web.create_table()
db_iot = iot.IOT_Database()

class User:
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # Initialize User Object
        # This Object is used to create user objects during signin and jwt_required operations
        def __init__(self, _id, username, password):
            self.id = _id
            self.username = username
            self.password = password

        @classmethod
        def find_by_username(cls, username_in):
            # Creating Web Database Object
            db_web = db.WEB_Database()
            db_web.create_table()
            db_iot = iot.IOT_Database()
            def return_data(message="", status_code=200):
                # Function to create a general form of response from various classes
                response = jsonify(message)
                response.status_code = status_code
                return response
            # Used to find the password for the given username. Called when signing in using usernmae
            value = db_web.get_password(username=username_in)
            print(username_in)
            print(value)
            if (value == 0):
                user = None
            else:
                user = cls(_id=value[0], username=value[1], password=value[2])
            return user

        def find_by_id(cls, _id):
                # Creating Web Database Object
            db_web = db.WEB_Database()
            db_web.create_table()
            db_iot = iot.IOT_Database()
            def return_data(message="", status_code=200):
                # Function to create a general form of response from various classes
                response = jsonify(message)
                response.status_code = status_code
                return response
            # Used to find the username for the given token. Called when using tokens
            value = db_web.find_id(username=username_in)
            if (value == 0):
                user = None
            else:
                user = cls(_id=value[0], username=value[1], password=value[2])
            return user

def return_data(message="", status_code=200):
    # Function to create a general form of response from various classes
    response = jsonify(message)
    response.status_code = status_code
    return response

class Resources:
    # Contains Resources for Web API part
    # These classes are called when respective API is called in App Class
    class Welcome(Resource):
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # Test Page
        def get(self):
            return return_data("Welcome to ISHA")


    class Signup(Resource):

        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()


        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # Used to Signup
        def post(self):
            data = request.get_json()
            x=db_web.insert_value(data['Name'],data['Username'],data['Password'])
            if x == 0:
                return return_data("Username Already Present",404)
            else:
                return return_data("Updated")

    class User:
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # Initialize User Object
        # This Object is used to create user objects during signin and jwt_required operations
        def __init__(self, _id, username, password):
            self.id = _id
            self.username = username
            self.password = password

        @classmethod
        def find_by_username(cls, username_in):
            # Creating Web Database Object
            db_web = db.WEB_Database()
            db_web.create_table()
            db_iot = iot.IOT_Database()
            def return_data(message="", status_code=200):
                # Function to create a general form of response from various classes
                response = jsonify(message)
                response.status_code = status_code
                return response
            # Used to find the password for the given username. Called when signing in using usernmae
            value = db_web.get_password(username=username_in)
            print(username_in)
            print(value)
            if (value == 0):
                user = None
            else:
                user = cls(_id=value[0], username=value[1], password=value[2])
            return user

        def find_by_id(cls, _id):
                # Creating Web Database Object
            db_web = db.WEB_Database()
            db_web.create_table()
            db_iot = iot.IOT_Database()
            def return_data(message="", status_code=200):
                # Function to create a general form of response from various classes
                response = jsonify(message)
                response.status_code = status_code
                return response
            # Used to find the username for the given token. Called when using tokens
            value = db_web.find_id(username=username_in)
            if (value == 0):
                user = None
            else:
                user = cls(_id=value[0], username=value[1], password=value[2])
            return user

    class Time_Interval_Update(Resource):
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        @jwt_required
        def post(self):
            data=request.get_json()
            db_web.insert_time_config(sno=data['Serial_Number'],time=data['Time_Interval'])
            return return_data()


    class Content(Resource):
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        @jwt_required
        def get(self):
            return return_data(str(db_iot.table_content()))


    class UpdateConfiguration(Resource):
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # Used to update MObile Number, Country Code and Time Intreval for the given mobile number
        @jwt_required
        def post(self):
            data = request.get_json()
            # Checking if Time Intreval is provided
            # If default Time intreval is not provided Time intreval = 1000
            db_web.insert_configuration(
                {'Serial_Number': data['Serial_Number'],'Time_Interval': data['Time_Intreval']})
            return return_data("Updated")

    class DeleteConfiguration_sno(Resource):
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # Used to delete all configuration information for all the devices
        @jwt_required
        def post(self):
            data = request.get_json()
            x = db_web.del_configuration_sno(data['Serial_Number'])
            if x == 0:
                return return_data("Serial Number Not Found", 404)
            return return_data("Updated")

    class DeleteConfiguration_mobile(Resource):
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # Used to delete specific mobile number for a specific device
        @jwt_required
        def post(self):
            data = request.get_json()
            x = db_web.del_configuration_mobile_number(data['Serial_Number'], data['Country_Code'],
                                                                 data['Phone_Number'])
            if x == 0:
                return return_data("Serial Number and Mobile Number pair not found", 404)
            return return_data("Updated")

    class UserLogin(Resource):
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        # User Login Class
        # Calls User class and accesses database to perform required operations
        @classmethod
        def post(cls):
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, help="The field cannot be left blank")
            parser.add_argument('password', type=str, required=True, help="The field cannot be left blank")
            data = parser.parse_args()
            data['username'] = str(data['username']).upper()
            data['password'] = str(data['password']).upper()
            user = User.find_by_username(data['username'])

            # this is what the `authenticate()` function did in security.py
            if user and safe_str_cmp(user.password, data['password']):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return jsonify({
                    'status': "200",
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })

            response = jsonify({"status": "401", "message": "Invalid Credentials!"})
            response.status_code = 401
            return response

    class UserLogout(Resource):
        # Creating Web Database Object
        db_web = db.WEB_Database()
        db_web.create_table()
        db_iot = iot.IOT_Database()
        def return_data(message="", status_code=200):
            # Function to create a general form of response from various classes
            response = jsonify(message)
            response.status_code = status_code
            return response
        BLACKLIST = set()
        # Performs user Logout operation
        # Blacklist's only Access Tokens
        @jwt_required
        def get(self):
            jti = get_raw_jwt()['jti']
            BLACKLIST.add(jti)
            response = jsonify({'message': 'Logged Out', 'status': 200})
            response.status_code = 200
            return response

    # A set to store logged out tokens to prevent misuse
    BLACKLIST = set()

    class TokenRefresh(Resource):
        # Used to create a new access tokens using refresh tokens
        @jwt_refresh_token_required
        def post(self):
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)
            refresh_token = create_refresh_token(current_user)
            return jsonify({'access_token': new_token, 'refresh_token': refresh_token, 'status': 200})

    class KillToken(Resource):
        # Used to black list refresh tokens
        @jwt_required
        def post(self):
            jti = get_raw_jwt()['jti']
            BLACKLIST.add(jti)
            return jsonify({'message': 'TokenKilled', 'status': 200})

