"""
WSGI wrapper for FastAPI on cPanel using Passenger.
This file allows your FastAPI app to run via cPanel's Setup Python App feature.
"""

import sys
import os

# Determine the path to the virtual environment
# cPanel creates virtual environments in ~/virtualenv/
# Adjust the path based on your actual setup
VENV_PATH = os.path.expanduser("~/virtualenv/app/3.11/bin/python3")

# If running under a different Python, restart using the virtual environment Python
if sys.executable != VENV_PATH:
    os.execl(VENV_PATH, VENV_PATH, *sys.argv)

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the FastAPI application
from api.main import app

# Passenger requires an 'application' variable
application = app

