from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

from app import db, Post, User
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

        auth_user_id = get_jwt_identity()

        post = Post()
        post.title = data['title']
        post.body = data['body']
        post.published_at = datetime.utcnow()
        post.created_at = datetime.utcnow()
        post.updated_at = datetime.utcnow()
        post.created_by = auth_user_id
        post.updated_by = auth_user_id
        db.session.add(post)
        db.session.commit()

        return jsonify({
            'status': True,
            'data': post
        })

    @staticmethod
    def get_all_posts():
        # Pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('limit', default=10, type=int)

        # Searching
        search_query = request.args.get('q')

        # created_by
        created_by = request.args.get('created_by')

        # Base query
        query = Post.query

        # populate
        populate = request.args.get('populate', '')

        # Apply search query
        if search_query:
            query = query.filter(
                or_(
                    Post.title.ilike(f'%{search_query}%'),
                    Post.body.ilike(f'%{search_query}%')
                )
            )

        if created_by:
            query = query.filter_by(created_by=created_by)

        # Paginate the results
        paginated_posts = query.paginate(page=page, per_page=per_page, error_out=False)

        post_list = []

        for post in paginated_posts.items:
            post_data = post

            if 'created_by' in populate:
                created_by = User.query.get(post.created_by)
                if created_by:
                    post_data.created_by = created_by

            if 'updated_by' in populate:
                updated_by = User.query.get(post.updated_by)
                if updated_by:
                    post_data.updated_by = updated_by

            post_list.append(post_data)

        # Prepare response
        response = {
            'results': post_list,
            'meta': {
                'total': paginated_posts.total,
                'page': paginated_posts.page,
                'pages': paginated_posts.pages
            }
        }

        return jsonify(response)

    @staticmethod
    def get_post(post_id):
        post = Post.query.get(post_id)
        if post:
            created_by = User.query.get(post.created_by)
            updated_by = User.query.get(post.updated_by)
            post.created_by = created_by
            post.updated_by = updated_by
            return jsonify(post)
        else:
            return jsonify({'message': 'Post not found'}), 404

    @staticmethod
    @jwt_required()
    @post_exist
    @admin_or_self_created
    def update_post(post_id):
        post_schema = {
            'title': {'type': 'string', 'empty': True, 'maxlength': 255},
            'body': {'type': 'string', 'empty': True}
        }

        data = validate_request_data(request, post_schema)
        if type(data) is tuple:
            return data

        post = Post.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        auth_user_id = get_jwt_identity()

        if 'title' in data:
            post.title = data['title']

        if 'body' in data:
            post.body = data['body']

        post.updated_at = datetime.utcnow()
        post.updated_by = auth_user_id
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
