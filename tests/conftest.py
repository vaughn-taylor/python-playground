# Add this configuration file to all tests
import sys
import os

# Add src/ to the system path so we can import hello.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))