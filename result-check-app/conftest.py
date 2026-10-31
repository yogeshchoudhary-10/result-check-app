# conftest.py — pytest configuration
# Ensures the app root is always on sys.path for all tests.
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
