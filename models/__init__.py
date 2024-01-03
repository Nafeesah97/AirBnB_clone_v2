#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""

import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

HBNB_TYPE_STORAGE = os.getenv("HBNB_TYPE_STORAGE", "fs")

if HBNB_TYPE_STORAGE == "db":
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
