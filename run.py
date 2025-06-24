from beram import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Determine environment
env = os.environ.get('FLASK_ENV', 'production')

# Create app with appropriate configuration
app = create_app(env)

if __name__ == '__main__':
    # Use debug=True only for development
    # For production, use a proper WSGI server like Gunicorn or Waitress
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))