import os
import sys
from flask import request, jsonify
from loguru import logger
from pathlib import Path
from datetime import datetime
import sys

def configure_logging(app):
    """Configure Loguru for the Flask application."""
    # Clear default logger
    logger.remove()
    
    # Format for log messages
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<magenta>Request ID: {extra[request_id]}</magenta> | "
        "<level>{message}</level>"
    )
    
    # Configure logger with request ID
    logger.configure(extra={"request_id": "N/A"})
    
    # Console logging
    logger.add(
        sys.stderr,
        level=app.config['LOG_LEVEL'],
        format=log_format,
        colorize=True,
        backtrace=True,
        diagnose=app.config.get('FLASK_ENV') == 'development'
    )
    
    # File logging (rotating)
    log_file = Path(app.config['LOG_FILE'])
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        str(log_file),
        rotation=app.config.get('LOG_ROTATION', '10 MB'),
        retention=app.config.get('LOG_RETENTION', '30 days'),
        level=app.config['LOG_LEVEL'],
        format=log_format,
        backtrace=True,
        diagnose=app.config.get('FLASK_ENV') == 'development',
        enqueue=True,  # Makes logging thread-safe
        encoding='utf-8'
    )
    
    # Add request context processor for request ID
    @app.before_request
    def before_request():
        from flask import g
        import uuid
        g.request_id = str(uuid.uuid4())
        logger.bind(request_id=g.request_id)
        
        # Log request details
        logger.info(f"Request: {request.method} {request.path}")
        
        # Log request data for non-GET requests
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if request.is_json:
                    logger.debug(f"Request JSON: {request.get_json(silent=True) or {}}")
                elif request.form:
                    logger.debug(f"Request Form: {dict(request.form)}")
                elif request.data:
                    logger.debug(f"Request Data: {request.data.decode('utf-8')}")
            except Exception as e:
                logger.warning(f"Failed to log request data: {str(e)}")
    
    @app.after_request
    def after_request(response):
        # Log response
        logger.info(
            f"Response: {response.status_code} {request.method} {request.path} "
            f"({request.content_length or 0}b)"
        )
        
        # Add request ID to response headers
        from flask import g
        response.headers['X-Request-ID'] = getattr(g, 'request_id', 'N/A')
        
        return response
    
    # Log unhandled exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.opt(exception=e).error(
            f"Unhandled Exception: {str(e)}\n"
            f"Request: {request.method} {request.path}\n"
            f"Headers: {dict(request.headers)}\n"
            f"Args: {dict(request.args)}\n"
            f"Form: {dict(request.form) if request.form else 'N/A'}"
        )
        
        if app.debug:
            # In debug mode, return detailed error information
            response = jsonify({
                'error': str(e),
                'type': e.__class__.__name__,
                'request_id': getattr(request, 'request_id', 'N/A')
            })
            response.status_code = 500
            return response
        
        # In production, return a generic error message
        return jsonify({
            'error': 'An internal server error occurred',
            'request_id': getattr(request, 'request_id', 'N/A')
        }), 500
    
    return logger
    
    return logger
