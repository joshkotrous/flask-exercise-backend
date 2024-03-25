import traceback

from flask import Blueprint, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

error_bp = Blueprint("errors", __name__)


@error_bp.app_errorhandler(NotFound)
def handle_not_found(err):
    print(traceback.format.exc())
    return jsonify({"message": "this resources is not found."}), 404


@error_bp.app_errorhandler(Exception)
def handle_generic_exception(err):
    print(traceback.format.exc())
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
    print(traceback.format.exc())
    return jsonify({"message": "Incorrect data format"}), 400
