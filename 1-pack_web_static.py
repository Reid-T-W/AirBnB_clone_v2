#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the
# contents of the web_static folder of the AirBnB Clone repo
from fabric.api import *
import os
import tarfile
import datetime

env.hosts = ['3.238.235.87', '100.26.133.150']
env.user = 'ubuntu'


def do_pack():
    """
    Collects the web_static files into a tar file and
    zips them
    """
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minute = today.minute
    second = today.second
    # Creating the directory if it does not exist
    try:
        os.makedirs("versions")
    except FileExistsError:
        pass
    try:
        # Creating the .tgz file
        name = "./versions/web_static_{}{}{}{}{}{}.tgz". \
               format(year, month, day, hour, minute, second)
        static_content = "./web_static/"
        with tarfile.open(name, "w:gz") as trzhandle:
            for root, dirs, files in os.walk(static_content):
                for f in files:
                    trzhandle.add(os.path.join(root, f))
        return name
    except Exception:
        return None
