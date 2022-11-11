#!/usr/bin/python3
""" This scripts starts a simple flask app with two routes """
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """ when the / route is requested this function runs"""
    return("Hello HBNB!")


@app.route('/hbnb')
def hbnb():
    """when the /hbnb route is requested this function runs"""
    return("HBNB")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
