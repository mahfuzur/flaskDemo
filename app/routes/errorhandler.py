from flask import jsonify

from app.routes import api


# Error handler for 400 Bad Request
@api.errorhandler(400)
def handle_bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400


# Error handler for 401 Unauthorized
@api.errorhandler(401)
def handle_unauthorized(error):
    return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401


# Error handler for 404 Not Found
@api.errorhandler(404)
def handle_not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404


# Error handler for 500 Internal Server Error
@api.errorhandler(500)
def handle_internal_server_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500
