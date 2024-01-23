#!/usr/bin/python3
"""importing necessay libraries"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """to start flask web application"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """displays HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """uses variables"""
    dis_text = text.replace('_', ' ')
    return 'C {}'.format(dis_text)

@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """uses variables"""
    dis_text = text.replace('_', ' ')
    return 'Python {}'.format(dis_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
