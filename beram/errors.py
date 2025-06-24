from flask import render_template
import logging
from logging.handlers import RotatingFileHandler
import os

def init_error_handlers(app):
    """Initialize error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('Server Error: %s', str(error))
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('400.html'), 400

def init_logging(app):
    """Set up logging for the application."""
    
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        # Set up file handler for logging
        file_handler = RotatingFileHandler('logs/beram.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        
        # Add handlers to app logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('BeRAM startup')
