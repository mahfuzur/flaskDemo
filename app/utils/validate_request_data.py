from cerberus import Validator
from flask import jsonify


def validate_request_data(request, schema):
    try:
        if request.content_type == 'application/json':
            data = request.get_json()
        elif request.content_type.startswith('multipart/form-data'):
            data = request.form
        else:
            return jsonify({'error': 'Unsupported content type'}), 400

        v = Validator(schema, allow_unknown=True)
        if not v.validate(data):
            errors = v.errors
            return jsonify({'errors': errors}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return data
