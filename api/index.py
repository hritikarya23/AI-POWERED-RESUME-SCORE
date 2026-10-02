import os
import sys

# Ensure parent directory is on sys.path so 'app' can be imported by Vercel serverless function
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
