from flask import Blueprint, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from backend.exceptions.invalid_password_error import InvalidPasswordError
from backend.exceptions.invalid_username_error import InvalidUsernameError

error_bp = Blueprint("errors", __name__)


@error_bp.app_errorhandler(NotFound)
def handle_not_found(err):
    # print(traceback.format.exc())
    return jsonify({"message": "this resources is not found."}), 404


@error_bp.app_errorhandler(Exception)
def handle_generic_exception(err):
    print(err)
    return (
        jsonify(
            {
                "message": "Unkown error. Please check the logs for more details."
                + str(err)
            }
        ),
        500,
    )


@error_bp.app_errorhandler(ValidationError)
def handle_invalid_data(error):
    print(error)
    return jsonify({"message": "Incorrect data format" + str(error)}), 400


@error_bp.app_errorhandler(InvalidUsernameError)
def handled_invalid_username(error):
    print(error)
    return jsonify({"message": str(error)}), 400


@error_bp.app_errorhandler(InvalidPasswordError)
def handled_invalid_password(error):
    print(error)
    return jsonify({"message": str(error)}), 400
