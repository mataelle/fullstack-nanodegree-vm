import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship('Item', back_populates="category")

    @property
    def serialize(self):
        ''' Return object data in easily serializable format '''
        return {
            'id': self.id,
            'name': self.name,
            'items': [i.serialize for i in self.items]
        }


class Item(Base):

    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1500))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    created = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        ''' Return object data in easily serializable format '''
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cat_id': self.category_id,
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
