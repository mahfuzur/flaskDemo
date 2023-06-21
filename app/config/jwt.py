from datetime import timedelta

from flask_jwt_extended import JWTManager


def initialize_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    JWTManager(app)
