from functools import wraps
from flask import jsonify

from app import Post, User


def post_exist(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        post = Post.query.get(kwargs['post_id'])
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        return func(*args, **kwargs)

    return decorated_function


def user_exist(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = User.query.get(kwargs['user_id'])
        if not user:
            return jsonify({'message': 'User not found'}), 404

        return func(*args, **kwargs)

    return decorated_function
