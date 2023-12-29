#!/usr/bin/python3

"""
Deploy archived content to web servers

"""

from fabric.api import env, run, task, put, hosts, sudo
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
        output = run("ls /tmp/").stdout.strip()
        for text in output.split():
            if text.startswith('web'):
                archive = text
                break
            continue

        # remove archive extension(eg .tgz)
        new_arc = archive[:-4]

        data = f"/data/web_static/releases/{new_arc}/"

        # create a directory for the archive
        run(f"sudo mkdir -p /data/web_static/releases/{new_arc}")

        # uncompress archive
        run(f'sudo tar -xf /tmp/{archive} -C {data}')

        # Delete the archive
        run(f'sudo rm -rf /tmp/{archive}')

        # move the web_static content into the newly created folder
        run(f"sudo cp -rf {data}web_static/* {data}")

        # remove web_static folder
        run(f"sudo rm -rf /data/web_static/releases/{new_arc}/web_static")

        # Delete symlink
        run('sudo rm -rf /data/web_static/current')

        current = "/data/web_static/current"
        # Create a new symlink to the location of uncompressed archive
        run(f'sudo ln -sf  /data/web_static/releases/{new_arc} {current}')

        return True

    except Exception:
        return False
