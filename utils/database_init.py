from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class InventoryType(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(256), nullable=False)
    inventory_type_id = (Integer, ForeignKey('inventory.id'))
    # inventory = relationship(InventoryType)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'inventory_type': self.inventory_type_id
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(1024), nullable=False)
    image = Column(String(64), nullable=False)
    ATK = Column(Integer, default=0)
    DEF = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    # category = relationship(Category)
    # user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_path': self.image,
            'attack_value': self.ATK,
            'defense_value': self.DEF,
            'category_id': self.category_id,
            'user_id': self.user_id
        }


engine = create_engine('sqlite:///InventoryCategories.db')

Base.metadata.create_all(engine)
