from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, current_user

from app import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # Verify the JWT token in the request
        current_user_id = get_jwt_identity()  # Get the current user ID

        # Retrieve the user from the database based on the current user ID
        user = User.query.get(current_user_id)

        # Check if the user exists and has the role 'admin'
        if user and user.role == 'admin':
            return fn(*args, **kwargs)  # User is authorized, proceed with the route

        # User is not authorized or does not exist, return an error response
        return jsonify({'error': 'Admin access required'}), 403

    return wrapper
