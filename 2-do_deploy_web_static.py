#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the
# contents of the web_static folder of the AirBnB Clone repo
from fabric.api import *
import os
import tarfile
import datetime
from os import path


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


def do_deploy(archive_path):
    """
    Distributes archive to web servers
    Attrs
        archive_path: the path to the archive file
    Returns
        True if all operations have been successfully
        completed else False
    """
    # Check if archive path exists locally
    if (path.exists(archive_path) is False):
        return False
    try:
        archive_name = os.path.basename(archive_path)
        archive_name_only = os.path.splitext(archive_name)[0]
        # placing the archives on the remote servers
        put(archive_path, "/tmp/{}".format(archive_name))
        # creating a the folder required for decompression
        run("mkdir -p /data/web_static/releases/{}/".format(archive_name_only))
        # extracting and decompressing the .tgz file
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".
            format(archive_name, archive_name_only))
        # delting the .tgz file
        run("rm /tmp/{}".format(archive_name))
        # move all contents from web_static to web_static_20221027225456
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static \
            /releases/{}".format(archive_name_only, archive_name_only))
        # deleting the old symbolic link
        run("rm /data/web_static/current")
        # creating a new symbolic link
        run("ln -s /data/web_static/releases/{} /data/web_static/current".
            format(archive_name_only))
        return True
    except Exception:
        return False
