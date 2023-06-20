from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


def initialize_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    jwt = JWTManager(app)
