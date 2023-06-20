from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, current_user

from app import User, Post


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


def admin_or_self_created(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Retrieve the current user's identity from the JWT token
        current_user_id = get_jwt_identity()

        # Check if the current user is an admin or the creator of the post
        is_admin = check_if_user_is_admin(current_user_id)
        is_self_created = check_if_user_created_post(current_user_id, kwargs['post_id'])

        # Check if the current user is an admin or the creator of the post
        if not (is_admin or is_self_created):
            return jsonify({'message': 'Admin access or post creator access required'}), 401

        return func(*args, **kwargs)

    return decorated_function


def check_if_user_is_admin(user_id):
    # Retrieve the user from the database based on the user ID
    user = User.query.get(user_id)

    # Check if the user exists and has the role of 'admin'
    if user and user.role == 'admin':
        return True

    return False


def check_if_user_created_post(user_id, post_id):
    # Retrieve the post from the database based on the post ID
    post = Post.query.get(post_id)

    # Check if the post exists and the user ID matches the creator ID
    if post and post.created_by == user_id:
        return True

    return False
