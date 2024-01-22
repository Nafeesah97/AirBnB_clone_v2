#!/usr/bin/python3
"""importing necessary libraries"""
from fabric.api import put, run, env, local
from datetime import datetime
import os


env.hosts = ['52.91.202.165', '52.87.222.58']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    local("mkdir -p versions")

    now = datetime.utcnow()
    date_str = now.strftime("%Y%m%d%H%M%S")

    archive_name = "web_static_{}.tgz".format(date_str)

    result = local(
            "tar -czvf versions/{} web_static".format(archive_name),
            capture=True)

    if result.failed:
        return None
    else:
        archive_path = os.path.join("versions", archive_name)
        print("web_static packed: {} -> {}Bytes".format(
            archive_path, os.path.getsize(archive_path)))
        return archive_path


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """

    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    archive_no_ext = os.path.splitext(archive_name)[0]
    remote_path = "/tmp/{}".format(archive_name)
    releases_path = "/data/web_static/releases/{}/".format(archive_no_ext)

    try:
        put(archive_path, remote_path)

        run("mkdir -p {}".format(releases_path))

        run("tar -xzf {} -C {}".format(remote_path, releases_path))

        run("rm {}".format(remote_path))

        run("mv {}/web_static/* {}".format(releases_path, releases_path))

        run("rm -rf {}/web_static".format(releases_path))

        run("rm -rf /data/web_static/current")

        run("ln -s {} /data/web_static/current".format(releases_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)
