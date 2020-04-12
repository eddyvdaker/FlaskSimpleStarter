
from flask import Blueprint, jsonify, render_template, request
from flask.wrappers import Response
from typing import Optional
from werkzeug.http import HTTP_STATUS_CODES

from src.database import rollback_db

bp = Blueprint('errors', __name__)

## Generic error handling functions for creating error responses

def _wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


def _html_error_response(status, error, message=None):
    return render_template('error.html', status=status, error=error,
        message=message), status


def _api_error_response(status, error, message=None):
    payload = {
        'status-code': status,
        'error': error
    }
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status
    return response


def error_response(status: int, message: Optional[str] = None) -> Response:
    """Helper function for returning more meaningful error messages.
    :param status: HTTP status code
    :param message: optional message
    """
    if type(status) is not int:
        status = status.code
    error = HTTP_STATUS_CODES.get(status, 'Unknown Error')

    if _wants_json_response():
        return _api_error_response(status, error, message)
    else:
        return _html_error_response(status, error, message)


## Error Handlers

@bp.app_errorhandler(400)
def bad_request(error) -> Response:
    """Errorhandler for 400 - Bad Request error."""
    return error_response(400)


@bp.app_errorhandler(403)
def forbidden(error) -> Response:
    """Errorhanlder for 403 - Forbidden error."""
    return error_response(403)


@bp.app_errorhandler(404)
def not_found(error) -> Response:
    """Errorhanlder for 404 - Not Found error."""
    return error_response(404)


@bp.app_errorhandler(500)
def internal_server_error(error) -> Response:
    """Errorhandler for 500 - Internal Server error."""
    rollback_db()
    return error_response(500)