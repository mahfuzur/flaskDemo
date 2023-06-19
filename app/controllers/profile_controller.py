from flask import Blueprint, jsonify, request


class ProfileController:
    @staticmethod
    def get_profile():
        data = request.get_json()
        # TODO: Validation and creation logic

    @staticmethod
    def set_profile():
        data = request.get_json()
        # TODO: Retrieve and transform data
