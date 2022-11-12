#!/usr/bin/python3
"""This module defines the Database Storage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import copy


class DBStorage():
    """DB Storage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """DBStorage initializer"""
        self.user = getenv("HBNB_MYSQL_USER", default=None)
        self.passwd = getenv("HBNB_MYSQL_PWD", default=None)
        self.db = getenv("HBNB_MYSQL_DB", default=None)
        self.host = getenv("HBNB_MYSQL_HOST", default=None)
        self.url = f"mysql+mysqldb://{self.user}:"\
                   f"{self.passwd}@{self.host}/{self.db}"
        self.__engine = create_engine(self.url, pool_pre_ping=True)
        if getenv("HBNB_ENV", default=None) == "test":
            # Drop all tables
            Base.metadata.drop_all(bind=DBStorage.__engine)

    def all(self, cls=None):
        """Returns all elements or elements filtered by class in DBStorage"""
        # If cls is passed as a string
        classes = {
            'State': State,
            'City': City,
            'User': User,
            'Place': Place,
            'Review': Review,
            'Amenity': Amenity
        }
        obj = {} 
        if cls is None:
            for key, val in classes.items():
                cls_objects = self.__session.query(val).all()
                copy_cls_objects = copy.deepcopy(cls_objects)
                for co in copy_cls_objects:
                    if '_sa_instance_state' in co.__dict__:
                        co.__dict__.pop("_sa_instance_state")
                    dicti = co.to_dict()
                    clss = dicti['__class__']
                    key = f"[{clss}] ({co.id})"
                    obj[key] = co
            return obj
        # If cls is passed as a string 
        elif isinstance(cls, str) and cls in classes:
            cls_objects = self.__session.query(classes[cls]).all()
        # If cls is passed as an object
        elif not isinstance(cls, str) and cls.__name__ in classes:
            cls_objects = self.__session.query(classes[cls.__name__]).all()
        copy_cls_objects = copy.deepcopy(cls_objects)
        for co in copy_cls_objects:
            if '_sa_instance_state' in co.__dict__:
                co.__dict__.pop("_sa_instance_state")
            dicti = co.to_dict()
            clss = dicti['__class__']
            key = f"{clss}.{co.id}"
            obj[key] = co
        return obj

    def new(self, obj):
        """Adds an object to the session"""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commits a session to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delets an object"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates a new session and schema"""
        self.session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False, )
        self.Session = scoped_session(self.session_factory)
        self.__session = self.Session()
        Base.metadata.create_all(self.__engine)

    def close(self):
        """Closes a session"""
        self.Session.remove();
