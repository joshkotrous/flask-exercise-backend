from flask import Blueprint, Response, jsonify, request

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    return "ok"
