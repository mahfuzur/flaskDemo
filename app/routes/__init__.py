from app.routes.route import web, api
from app.routes.errorhandler import *


def register_routes(app):
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/v1')
