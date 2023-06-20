from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app import db, Post
from app.middlewares import post_exist, admin_or_self_created
from app.utils import validate_request_data


class PostController:
    @staticmethod
    @jwt_required()
    def create_post():
        post_schema = {
            'title': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
            'body': {'type': 'string', 'required': True, 'empty': False}
        }

        data = validate_request_data(request, post_schema)
        if type(data) is tuple:
            return data

        post = Post()
        post.title = data['title']
        post.body = data['body']
        post.published_at = datetime.utcnow()
        post.created_at = datetime.utcnow()
        post.updated_at = datetime.utcnow()
        post.created_by = 1
        post.updated_by = 1
        db.session.add(post)
        db.session.commit()

        return jsonify({
            'status': True,
            'data': post
        })

    @staticmethod
    def get_all_posts():
        posts = Post.query.all()
        return jsonify(posts)

    @staticmethod
    def get_post(post_id):
        post = Post.query.get(post_id)
        if post:
            return jsonify(post)
        else:
            return jsonify({'message': 'Post not found'}), 404

    @staticmethod
    @jwt_required()
    @post_exist
    @admin_or_self_created
    def update_post(post_id):
        post_schema = {
            'title': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
            'body': {'type': 'string', 'required': True, 'empty': False}
        }

        data = validate_request_data(request, post_schema)
        if type(data) is tuple:
            return data

        post = Post.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        post.title = data['title']
        post.body = data['body']
        post.updated_at = datetime.utcnow()
        post.updated_by = 1
        db.session.add(post)
        db.session.commit()

        return jsonify({
            'status': True,
            'data': post
        })

    @staticmethod
    @jwt_required()
    @post_exist
    @admin_or_self_created
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return jsonify({'message': 'Post deleted successfully'})
        else:
            return jsonify({'message': 'Post not found'}), 404
