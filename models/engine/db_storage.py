#!/usr/bin/python3
"""
To create database storage
"""
import os
from sqlalchemy import (create_engine, text)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User
from models.state import State
from models.base_model import Base
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

    def all(self, cls=None):
        """all objects depending of the class name"""
        classes = {"State": State, "City": City}
        res = {}

        if cls == None:
            for i,j in classes.items():
                query = self.__session.query(j).all()
                for objs in query:
                    keys = objs.__class__.__name__ + '.' + objs.id 
                    res[keys] = objs
        
        elif cls not in classes.values():
            return res

        else:
            query = self.__session.query(cls).all()
            for objs in query:
                keys = objs.__class__.__name__ + '.' + objs.id 
                res[keys] = objs
        
        return res

    def new(self, obj):
        """add the object to the current database"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj != None:
            (self.__session.query(type(obj)).
             filter(type(obj).id == obj.id).
             delete(synchronize_session='fetch'))

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()
