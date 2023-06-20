from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.controllers import AuthController, PostController, UserController, ProfileController

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)


@web.route("/", methods=['GET'])
def index():
    return jsonify({'title': 'Flask Demo API!'})


auth_controller = AuthController()
api.route('/login', methods=['POST'])(auth_controller.login)
api.route('/register', methods=['POST'])(auth_controller.register)

profile_controller = ProfileController()

api.route('/profile', methods=['GET'])(profile_controller.get_profile)
api.route('/profile', methods=['POST'])(profile_controller.set_profile)

post_controller = PostController()
api.route('/posts', methods=['POST'])(post_controller.create_post)
api.route('/posts', methods=['GET'])(post_controller.get_all_posts)
api.route('/posts/<int:post_id>', methods=['GET'])(post_controller.get_post)
api.route('/posts/<int:post_id>', methods=['PUT'])(post_controller.update_post)
api.route('/posts/<int:post_id>', methods=['DELETE'])(post_controller.delete_post)

user_controller = UserController()
api.route('/users', methods=['POST'])(user_controller.create_user)
api.route('/users', methods=['GET'])(user_controller.get_all_users)
api.route('/users/<int:user_id>', methods=['GET'])(user_controller.get_user)
api.route('/users/<int:user_id>', methods=['PUT'])(user_controller.update_user)
api.route('/users/<int:user_id>', methods=['DELETE'])(user_controller.delete_user)
