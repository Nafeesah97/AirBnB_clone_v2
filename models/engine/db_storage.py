#!/usr/bin/python3
"""
To create database storage
"""
import os
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker


class DBStorage():
    """A class of databases storage"""
    __engine = None
    __session = None

    def __init__(self):
        """To initialize"""
        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, database
        ), pool_pre_ping=True)

        Session = sessionmaker()
        Session.configure(bind=self.__engine)
        self.__session = Session()

        if os.environ.get('HBNB_ENV') == 'test':
            self.__engine.table_names()
            self.__engine.drop_all()
