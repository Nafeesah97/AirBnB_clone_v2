#!/usr/bin/python3
"""import necessary libraries"""
from fabric.api import local
from datetime import datetime
import os


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
