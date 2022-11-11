#!/usr/bin/python3
"""This script starts a flask app that handles route with variables """
from flask import Flask, escape
app = Flask(__name__)


@app.route('/')
def index():
    """ when the / route is requested this function runs"""
    return("Hello HBNB!")


@app.route('/hbnb')
def hbnb():
    """when the /hbnb route is requested this function runs"""
    return("HBNB")


@app.route('/c/<text>')
def c_dynamic(text):
    """
    when the dynamic route /c/<text>
    is requested this function runs
    """
    text = text.replace('_', ' ')
    return("C %s" % escape(text))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
