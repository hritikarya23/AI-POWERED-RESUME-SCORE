import os
import sys

# Ensure root directory is on Python module search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app.main import app

# For Vercel Serverless Function compatibility
application = app
