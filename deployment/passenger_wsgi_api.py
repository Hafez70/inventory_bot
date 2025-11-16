"""
WSGI wrapper for FastAPI on cPanel using Passenger.
This file should be placed in the application root directory.
"""

import sys
import os

# Add the application root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI application
from api.main import app

# Passenger requires an 'application' variable
application = app

