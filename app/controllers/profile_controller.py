from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


class ProfileController:
    @staticmethod
    @jwt_required()
    def get_profile():
        current_user = get_jwt_identity()
        return jsonify(message='Access granted for user {}'.format(current_user)), 200

    @staticmethod
    @jwt_required()
    def set_profile():
        data = request.get_json()
        # TODO: Retrieve and transform data
