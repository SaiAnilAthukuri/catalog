import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)   


class MobileCompanyName(Base):
    __tablename__ = 'mobilecompanyname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="mobilecompanyname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class MobileName(Base):
    __tablename__ = 'mobilename'
    id = Column(Integer, primary_key=True)
    modelname = Column(String(350), nullable=False)
    processor = Column(String(150))
    ram = Column(Integer)
    rom = Column(Integer)
    price = Column(String(10))
    screensize = Column(Integer)
    rating = Column(String(200))
    date = Column(DateTime, nullable=False)
    mobilecompanynameid = Column(Integer, ForeignKey('mobilecompanyname.id'))
    mobilecompanyname = relationship(
        MobileCompanyName, backref=backref(
            'mobilename', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="mobilename")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'modelname': self. modelname,
            'processor': self. processor,
            'ram': self. ram,
            'rom': self. rom,
            'price': self. price,
            'screensize': self. screensize,
            'rating': self. rating,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///mobiles.db')
Base.metadata.create_all(engin)
