import bcrypt
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import User
from app.config.db import db
from app.utils import validate_request_data


class ProfileController:
    @staticmethod
    @jwt_required()
    def get_profile():
        auth_id = get_jwt_identity()
        user = User.query.get(auth_id)
        if user:
            return jsonify(user)
        else:
            return jsonify({'message': 'User not found'}), 404

    @staticmethod
    @jwt_required()
    def set_profile():
        auth_id = get_jwt_identity()
        profile_schema = {
            'full_name': {'type': 'string', 'empty': False},
            'email': {'type': 'string', 'empty': False},
        }

        data = validate_request_data(request, profile_schema)
        if type(data) is tuple:
            return data

        user = User.query.get(auth_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'email' in data:
            # Check if the email already exists for another user
            existing_user = User.query.filter(User.email == data['email'], User.id != auth_id).first()
            if existing_user:
                return jsonify({'message': 'Email already exists',
                                'errors': {
                                    'email': 'Email already exists'
                                }}), 400
            user.email = data['email']

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'status': True,
            'data': user
        })

    @staticmethod
    @jwt_required()
    def change_password():
        auth_id = get_jwt_identity()
        password_schema = {
            'old_password': {'type': 'string', 'empty': False, 'required': True},
            'new_password': {'type': 'string', 'empty': False, 'required': True},
        }

        data = validate_request_data(request, password_schema)
        if type(data) is tuple:
            return data

        user = User.query.get(auth_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Verify the old password
        if not bcrypt.checkpw(data['old_password'].encode('utf-8'), user.encrypted_password.encode('utf-8')):
            return jsonify({'message': 'Invalid old password'}), 400

        # Check if the old password and new password are the same
        if data['old_password'] == data['new_password']:
            return jsonify({'message': 'Old password and new password must be different'}), 400

        # Update the password with the new one
        user.encrypted_password = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt())
        db.session.commit()

        return jsonify({'message': 'Password changed successfully'})
