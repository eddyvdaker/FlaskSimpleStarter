import logging
from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    """A custom Formatter for logging."""

    def format(self, record):
        record.url = None
        record.remote_addr = None
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        return super().format(record)
