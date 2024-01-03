#!/usr/bin/python3
""" DB Storage Engine """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base

class DBStorage:
    """ DB Storage Engine """
    __engine = None
    __session = None

    def __init__(self):
        """ Constructor for DBStorage """
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default="localhost")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, database),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """ Query on the current database session """
        from models import storage
        classes = ["User", "State", "City", "Amenity", "Place", "Review"]
        objects = {}

        if cls is None:
            for class_name in classes:
                query = self.__session.query(eval(class_name))
                for obj in query.all():
                    key = "{}.{}".format(class_name, obj.id)
                    objects[key] = obj
        else:
            query = self.__session.query(eval(cls))
            for obj in query.all():
                key = "{}.{}".format(cls, obj.id)
                objects[key] = obj

        return objects

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create the current database session """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
