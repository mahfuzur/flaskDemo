from flask import Blueprint

from app.controllers.auth_controller import register, login

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)


@web.route("/", methods=['GET'])
def hello_world1():
    return '<p>Hello, Flask API!</p>'


api.route('/login', methods=['POST'])(login)
api.route('/register', methods=['POST'])(register)


# Register the blueprint with the Flask app
def register_routes(app):
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/v1')
