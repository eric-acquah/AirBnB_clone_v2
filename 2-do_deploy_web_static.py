#!/usr/bin/python3

"""
Deploy archived content to web servers

"""

from fabric.api import env, sudo, task, put, hosts
import os


@task
@hosts(["107.23.160.42", "52.91.131.122"])
def do_deploy(archive_path):
    """
    Deploy the contents of an archive to a remote web server

    Args:
        archive_path (str) - path to the archive on the local machine

    Return:
        True if successful else false
    """
    # Check if the path to archive exists
    if os.path.exists(archive_path) is False:
        return False

    try:
        # setup connetcion with remote host
        env.use_ssh_config = False
        env.user = "ubuntu"
        env.key_filename = os.path.expanduser("~/.ssh/school")
        env.port = 22

        # upload archive to remote hosts
        put(f'{archive_path}', '/tmp/')

        # extract the archive filename
        output = sudo("ls /tmp/").stdout.strip()
        for text in output.split():
            if text.startswith('web'):
                archive = text
                break
            continue

        # remove archive extension(eg .tgz)
        new_arc = archive[:-4]

        # create a directory for the archive
        sudo(f"mkdir -p /data/web_static/releases/{new_arc}")

        # uncompress archive
        sudo(f'tar -xf /tmp/{archive} -C /data/web_static/releases/{new_arc}/')

        # Delete the archive
        sudo(f'rm -rf /tmp/{archive}')

        data = f"/data/web_static/releases/{new_arc}/"
        # move the web_static content into the newly created folder
        sudo(f"cp -rf /data/web_static/releases/{new_arc}/web_static/* {data}")

        # remove web_static folder
        sudo(f"rm -rf /data/web_static/releases/{new_arc}/web_static")

        # Delete symlink
        sudo('rm -rf /data/web_static/current')

        current = "/data/web_static/current"
        # Create a new symlink to the location of uncompressed archive
        sudo(f'ln -sf  /data/web_static/releases/{new_arc} {current}')

        return True

    except Exception:
        return False
