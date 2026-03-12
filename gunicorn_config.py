import multiprocessing

# Configuration Gunicorn optimisée pour Render
bind = "0.0.0.0:10000"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Performance
preload_app = True
max_requests = 1000
max_requests_jitter = 50
