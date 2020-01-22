# Documented at
# http://docs.gunicorn.org/en/latest/settings.html
import os

# Address where the app will be served at
bind = "127.0.0.1:5000"

# Worker setup
workers = 1
# Increase this if loading db cache takes too long
timeout = 120

# Enable logging at dir logs and pipe output there
DIR = os.path.dirname(os.path.abspath(__file__))
access_logfile = os.path.join(DIR, "logs/access.log")
error_logfile = os.path.join(DIR, "logs/error.log")
capture_output = True
# Detach from the console and run in background
daemon = True
