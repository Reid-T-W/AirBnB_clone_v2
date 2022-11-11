#!/usr/bin/python3
"""This script starts a flask app that handles route with variables """
from flask import Flask, escape, redirect, url_for
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


@app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_dynamic(text):
    """
    when the dynamic route /python/<text>
    is requested this function runs
    """
    text = text.replace('_', ' ')
    return("Python %s" % escape(text))


@app.route('/number/<int:n>')
def number_dynamic(n):
    """
    when the dynamic route /number/<int:n>
    is requested this function runs
    """
    return("%d is a number" % n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
