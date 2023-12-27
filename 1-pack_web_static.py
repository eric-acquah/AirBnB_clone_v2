#!/usr/bin/python3

"""
Create an Archeive

"""

from fabric.api import task
from fabric.api import local
import os


@task
def do_pack():
    """ Create an archeive """

    # create the directory
    local("mkdir -p versions")

    # get the current timestamp
    timestmp = local("date +%Y%m%d%H%M%S", capture=True).stdout.strip()

    # build the path
    arc_path = os.path.join("versions", f"web_static_{timestmp}.tgz")

    # Create the archeive
    local(f"tar -cvzf {arc_path} web_static")

    # confirm execution success
    if os.path.exists(arc_path):
        return f"{arc_path}"
    else:
        return None
