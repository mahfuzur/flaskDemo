import bcrypt
from flask import jsonify, request
from flask_jwt_extended import create_access_token

from app import User
from app.config.db import db
from app.utils import validate_request_data


class AuthController:

    @staticmethod
    def login():
        login_schema = {
            'email': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
            'password': {'type': 'string', 'required': True, 'empty': False}
        }

        data = validate_request_data(request, login_schema)
        if type(data) is tuple:
            return data

        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), user.encrypted_password.encode('utf-8')):
            # Passwords match, generate and return an access token or any other authentication response
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'token': access_token,
                'user': user
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    @staticmethod
    def register():
        register_schema = {
            'full_name': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
            'email': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
            'password': {'type': 'string', 'required': True, 'empty': False}
        }

        data = validate_request_data(request, register_schema)
        if type(data) is tuple:
            return data

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists',
                            'errors': {
                                'email': 'Email already exists'
                            }}), 400

        user = User()
        user.full_name = data['full_name']
        user.email = data['email']
        user.encrypted_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user.role = 'user'

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        return jsonify({
            'token': access_token,
            'user': user
        })
