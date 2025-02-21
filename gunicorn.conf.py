# Recommended settings for production
workers = 4  # Number of worker processes (2-4 x NUM_CORES)
bind = "0.0.0.0:8000"  # IP and port to bind
timeout = 120  # Worker timeout in seconds
keepalive = 5  # Keepalive timeout
worker_class = "sync"  # Worker class (sync, gevent, etc.)
accesslog = "-"  # Access log file ("-" for stdout)
errorlog = "-"   # Error log file ("-" for stderr)
loglevel = "info"  # Log level