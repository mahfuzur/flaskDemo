import bcrypt
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

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
        # Pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('limit', default=10, type=int)

        # Filtering
        role = request.args.get('role')

        # Searching
        search_query = request.args.get('q')

        # Sorting
        sort_param = request.args.get('sort')
        sort_fields = []
        if sort_param:
            sort_fields = sort_param.split(',')

        # Base query
        query = User.query

        # Apply filters
        if role:
            query = query.filter_by(role=role)

        # Apply search query
        if search_query:
            query = query.filter(
                or_(
                    User.full_name.ilike(f'%{search_query}%'),
                    User.email.ilike(f'%{search_query}%'),
                    User.role.ilike(f'%{search_query}%')
                )
            )

        # Apply sorting
        for field in sort_fields:
            if field.startswith('-'):
                # Descending order
                sort_field = field[1:]
                if hasattr(User, sort_field):
                    query = query.order_by(getattr(User, sort_field).desc())
                else:
                    return jsonify({'error': f'Invalid sort field: {sort_field}'}), 400
            else:
                # Ascending order
                if hasattr(User, field):
                    query = query.order_by(getattr(User, field))
                else:
                    return jsonify({'error': f'Invalid sort field: {field}'}), 400

        # Paginate the results
        paginated_users = query.paginate(page=page, per_page=per_page, error_out=False)

        # Prepare response
        response = {
            'results': paginated_users.items,
            'meta': {
                'total': paginated_users.total,
                'page': paginated_users.page,
                'pages': paginated_users.pages
            }
        }

        return jsonify(response)

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
            # Check if the email already exists for another user
            existing_user = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing_user:
                return jsonify({'message': 'Email already exists',
                                'errors': {
                                    'email': 'Email already exists'
                                }}), 400

            user.email = data['email']

        if 'role' in data:
            user.role = data['role']
        if 'password' in data:
            user.encrypted_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        db.session.add(user)
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
