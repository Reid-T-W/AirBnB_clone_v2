#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
   
    @property
    def cities(self):
        from models import storage
        from models.city import City
        filtered_objs=[]
        objs = storage.all(City)
        for key, value in objs.items():
            if value.state_id == self.id:
                filtered_objs.append(value)
        return filtered_objs
