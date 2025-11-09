from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required, roles_required, current_user

from controllers.user_datastore import user_datastore
from controllers.database import db

class LoginAPI(Resource):
    def post(self):

        login_credentials = request.get_json()

        # data validation
        if not login_credentials:
            result = {
                'message': 'Login credentials are required.',
            }
            return make_response(jsonify(result), 400)
        
        email = login_credentials.get('email', None)
        password = login_credentials.get('password', None)

        if not email or not password:
            result = {
                'message': 'Both email and password are required.',
            }
            return make_response(jsonify(result), 400)
        
        user = user_datastore.find_user(email=email)

        if not user:
            result = {
                'message': 'User not found.',
            }
            return make_response(jsonify(result), 404)
        
        if not utils.verify_password(password, user.password):
            result = {
                'message': 'Invalid password.',
            }
            return make_response(jsonify(result), 401)
        
        auth_token = user.get_auth_token()

        utils.login_user(user)

        response = {
            'message': 'Login successful.',
            'user_details': {
                'email': user.email,
                'roles': [role.name for role in user.roles],
                'auth_token': auth_token
            }
        }

        return make_response(jsonify(response), 200)

class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        response = {
            'message': 'Logout successful.'
        }
        return make_response(jsonify(response), 200)
    
class RegisterAPI(Resource):
    def post(self):
        creads = request.get_json()

        if not creads:
            result = {
                'message': 'Registration details are required.',
            }
            return make_response(jsonify(result), 400)
        
        email = creads.get('email', None)
        password = creads.get('password', None)

        if not email or not password:
            result = {
                'message': 'Both email and password are required.',
            }
            return make_response(jsonify(result), 400)
        
        if user_datastore.find_user(email=email):
            result = {
                'message': 'User already exists.',
            }
            return make_response(jsonify(result), 409)

        user_role = user_datastore.find_role(name='user')

        user_datastore.create_user(
            email=email,
            password=password,
            roles=[user_role]
        )

        db.session.commit()

        response = {
            'message': 'User registered successfully.',
            'user_details': {
                'email': email,
                'roles': [user_role.name]
            }
        
        }

        return make_response(jsonify(response), 201)