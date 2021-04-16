#!/usr/bin/python3
"""
 Fabric script that generates a .tgz archive
 from the contents of the web_static folder of
 your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import *
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['34.229.218.206', '54.210.76.219']


def do_deploy(archive_path):
    """
        Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    _path = archive_path.split("/")
    path_no_ext = _path[1].split(".")[0]

    try:
        put(archive_path, "/tmp")
        run("sudo mkdir -p /data/web_static/releases/" + path_no_ext + "/")
        run("sudo tar -xzf /tmp/" + path_no_ext + ".tgz" +
            " -C /data/web_static/releases/" + path_no_ext + "/")
        run("sudo rm /tmp/" + path_no_ext + ".tgz")
        run("sudo mv /data/web_static/releases/" + path_no_ext +
            "/web_static/* /data/web_static/releases/" + path_no_ext + "/")
        run("sudo rm -rf /data/web_static/releases/" +
            path_no_ext + "/web_static")
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/" + path_no_ext +
            "/ /data/web_static/current")
        return True

    except Exception:
        return False
