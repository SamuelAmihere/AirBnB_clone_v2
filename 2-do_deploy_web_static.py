#!/usr/bin/python3
import os
from datetime import datetime
from fabric.api import env, local, put, run


env.hosts = ['35.168.3.7', '100.25.170.135']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """ distributes an archive to my web servers """
    if not (os.path.exists(archive_path)):
        return False

    try:
        # upload archive_path to server
        put(archive_path, "/tmp")

        # Uncompress file into server folder
        file = archive_path.split("/")[-1].split(".")[0]
        dest_folder = "/data/web_static/releases/{}".format(file)
        src_file = "/tmp/{}.tgz".format(file)
        run("sudo mkdir -p {}".format(dest_folder))
        run("sudo tar -xzf {} -C {}/".format(src_file, dest_folder))
        run("sudo rm {}".format(src_file))

        # move contents from dest_folder/web_static into host web_static
        run("sudo mv {}/web_static/* {}".format(dest_folder, dest_folder))

        # remove web_static folder from dest_folder
        run("sudo rm -rf {}/web_static".format(dest_folder))

        # delete sym link
        run('sudo rm -rf /data/web_static/current')

        # new sym link to the current release dest_folder
        run('sudo ln -s {}/ /data/web_static/current'.format(dest_folder))
    except Exception as e:
        False
    return True
