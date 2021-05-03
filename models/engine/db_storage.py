#!/usr/bin/python3
"""DBstorage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def get_url():
    """Get url for the engine"""

    value = os.getenv("HBNB_MYSQL_USER")
    value1 = os.getenv("HBNB_MYSQL_PWD")
    value2 = os.getenv("HBNB_MYSQL_HOST")
    value3 = os.getenv("HBNB_MYSQL_DB")

    u = 'mysql+mysqldb://{}:{}@{}:3306/{}'\
        .format(value, value1, value2, value3)

    return u


class DBStorage():
    """Engine Creator"""
    __engine = None
    __session = None

    def __init__(self):
        """Init"""
        self.__engine = create_engine(get_url(), pool_pre_ping=True)

        value4 = os.getenv("HBNB_ENV")
        if value4 == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ALL function"""
        table = [User, State, City, Amenity, Place, Review]
        """ table = [State, City, User, Place] """
        new_dict = {}
        if cls is not None:
            if type(cls) is str:
                cls = eval(cls)
            all_data = self.__session.query(cls)
            for row in all_data:
                key = cls.__name__ + "." + row.id
                new_dict[key] = row
            return new_dict

        else:
            for indx in table:
                for obj in self.__session.query(indx):
                    key = indx.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
                return new_dict

    def new(self, obj):
        """Function that add new objects in current session"""
        self.__session.add(obj)

    def save(self):
        """Commit all the changes in the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete objects from the current session"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """create all tables in the database
            create the current database session
        """
        Session_new = sessionmaker(expire_on_commit=False)
        Session_new.configure(bind=self.__engine)
        Session = scoped_session(Session_new)
        self.__session = Session()
        Base.metadata.create_all(self.__engine)

    def close(self):
        """method on the private session attribute"""
        self.__session.close()
