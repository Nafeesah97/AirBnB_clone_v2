#!/usr/bin/python3
"""importing necessay libraries"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello:
    """to start flask web application"""
    return 'Hello HBNB!'