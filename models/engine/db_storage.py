#!/usr/bin/python3
"""This module manage database connection and Queries"""
import os
from sqlalchemy import create_engine


class DBStorage:
    """This class manages storage of hbnb models in Database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializer"""
        from models.base_model import Base
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(
                                         os.getenv("HBNB_MYSQL_USER"),
                                         os.getenv("HBNB_MYSQL_PWD"),
                                         os.getenv("HBNB_MYSQL_HOST"),
                                         os.getenv("HBNB_MYSQL_DB"),
                                         pool_pre_ping=True
                                         )
                                      )
        if os.getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Querying all objects"""
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        from models.user import User
        rows = []
        if cls:
            rows = self.__session.query(cls)
        else:
            rows += self.__session.query(State)
            rows += self.__session.query(City)
            rows += self.__session.query(Place)
            rows += self.__session.query(Amenity)
            rows += self.__session.query(Review)
            rows += self.__session.query(User)
        return {row.__class__.__name__ + '.' + row.id: row for row in rows}

    def new(self, obj):
        """Add a new object to current session database"""
        self.__session.add(obj)

    def save(self):
        """Commits changes to the current session database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current session database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads current session instance"""
        from sqlalchemy.orm import sessionmaker, scoped_session
        from models.base_model import Base
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
        )
        self.__session = Session()

    def close(self):
        """ call remove() method on the private session attribute
        (self.__session) or close() on the class Session """
        self.__session.close()
