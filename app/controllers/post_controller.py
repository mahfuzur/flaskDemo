from datetime import datetime

from cerberus import Validator
from flask import jsonify, request

from app import db, Post


class PostController:
    @staticmethod
    def create_post():
        post_schema = {
            'title': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
            'body': {'type': 'string', 'required': True, 'empty': False}
        }

        try:
            if request.content_type == 'application/json':
                data = request.get_json()
            elif request.content_type.startswith('multipart/form-data'):
                data = request.form
            else:
                return jsonify({'error': 'Unsupported content type'}), 400

            v = Validator(post_schema, allow_unknown=True)
            if not v.validate(data):
                errors = v.errors
                return jsonify({'errors': errors}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

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
    def update_post(post_id):
        post_schema = {
            'title': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
            'body': {'type': 'string', 'required': True, 'empty': False}
        }

        try:
            if request.content_type == 'application/json':
                data = request.get_json()
            elif request.content_type.startswith('multipart/form-data'):
                data = request.form
            else:
                return jsonify({'error': 'Unsupported content type'}), 400

            v = Validator(post_schema, allow_unknown=True)
            if not v.validate(data):
                errors = v.errors
                return jsonify({'errors': errors}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

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
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return jsonify({'message': 'Post deleted successfully'})
        else:
            return jsonify({'message': 'Post not found'}), 404
