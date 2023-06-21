import bcrypt
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import User
from app.config.db import db
from app.middlewares import admin_required
from app.utils import validate_request_data


class UserController:
    @staticmethod
    @jwt_required()
    @admin_required
    def create_user():
        user_schema = {
            'full_name': {'type': 'string', 'required': True, 'empty': False},
            'email': {'type': 'string', 'required': True, 'empty': False},
            'role': {'type': 'string', 'allowed': ['admin', 'user'], 'required': True, 'empty': False},
            'password': {'type': 'string', 'required': True, 'empty': False}
        }

        data = validate_request_data(request, user_schema)
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
        user.role = data['role']

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'status': True,
            'data': user
        })

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return jsonify(users)

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user)
        else:
            return jsonify({'message': 'User not found'}), 404

    @staticmethod
    @jwt_required()
    @admin_required
    def update_user(user_id):
        user_schema = {
            'full_name': {'type': 'string', 'empty': False},
            'email': {'type': 'string', 'empty': False},
            'role': {'type': 'string', 'allowed': ['admin', 'user']},
            'password': {'type': 'string', 'empty': False}
        }

        data = validate_request_data(request, user_schema)
        if type(data) is tuple:
            return data

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'email' in data:
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'password' in data:
            user.encrypted_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        db.session.commit()

        return jsonify({
            'status': True,
            'data': user
        })

    @staticmethod
    @jwt_required()
    @admin_required
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        auth_user_id = get_jwt_identity()
        if auth_user_id == user_id:
            return jsonify({'message': 'Self-deletion is not allowed'}), 403

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'})
