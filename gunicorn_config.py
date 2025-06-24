import multiprocessing
import os

# Bind to 0.0.0.0:8000 by default
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')

# Number of worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Worker class
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'gevent')

# Timeout in seconds
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 30))

# Number of requests a worker will process before restarting
max_requests = int(os.environ.get('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.environ.get('GUNICORN_MAX_REQUESTS_JITTER', 50))

# Process name
proc_name = 'beram_gunicorn'

# Access log - disable if behind a proxy
accesslog = os.environ.get('GUNICORN_ACCESS_LOG', '-')

# Error log
errorlog = os.environ.get('GUNICORN_ERROR_LOG', '-')

# Log level
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')

# Whether to send flask output to the error log
capture_output = True

# Enable statsd metrics
statsd_host = os.environ.get('STATSD_HOST', None)
statsd_prefix = 'beram'
