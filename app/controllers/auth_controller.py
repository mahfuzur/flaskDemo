from flask import request, jsonify


def login():
    # Get the data from the request body
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    return jsonify({
        email: email,
        password: password
    })


def register():
    # Get the data from the request body
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    return jsonify({
        full_name: full_name,
        email: email,
        password: password
    })
