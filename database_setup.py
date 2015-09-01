from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# to tables in a SQL database
"""database_setup.py: This file contains code for Object Relational Mapping of"""
"""                   User, Category, and Item classes to SQl tables in a database."""

Base = declarative_base()


# User table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return user data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


# Category table
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    items = relationship("Item")

    @property
    def serialize(self):
        """Return category data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'Item': self.serializeItems
        }

    @property
    def serializeItems(self):
        """Return each item data in easily serializeable format"""
        return [item.serialize for item in self.items]


# Table to hold items associated with each Category
class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    image = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return item data in easily serializeable format"""
        return {
            'cat_id': self.category.id,
            'description': self.description,
            'id': self.id,
            'name': self.name,
            "image": self.image
        }

engine = create_engine('sqlite:///catalogItems.db')


Base.metadata.create_all(engine)
