from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class InventoryType(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    inventory_type_id = Column(Integer, ForeignKey("inventory.id"))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    inventory = relationship(
        "InventoryType", foreign_keys=[inventory_type_id])
    user = relationship(
        "User", foreign_keys=[user_id])

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "inventory_type": self.inventory_type_id
        }


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(String(512), nullable=False)
    image = Column(String(64), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    category = relationship(
        "Category", foreign_keys=[category_id])
    user = relationship(
        "User", foreign_keys=[user_id])

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_path": self.image,
            "category_id": self.category_id,
        }


class Skin(Base):
    __tablename__ = "skin"

    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])

    head_id = Column(Integer, ForeignKey("item.id"))
    torso_id = Column(Integer, ForeignKey("item.id"))
    legs_id = Column(Integer, ForeignKey("item.id"))
    hands_id = Column(Integer, ForeignKey("item.id"))
    feet_id = Column(Integer, ForeignKey("item.id"))
    left_hand_id = Column(Integer, ForeignKey("item.id"))
    right_hand_id = Column(Integer, ForeignKey("item.id"))
    companion_id = Column(Integer, ForeignKey("item.id"))

    head = relationship(
        "Item", foreign_keys=[head_id])
    torso = relationship(
        "Item", foreign_keys=[torso_id])
    legs = relationship(
        "Item", foreign_keys=[legs_id])
    hands = relationship(
        "Item", foreign_keys=[hands_id])
    feet = relationship(
        "Item", foreign_keys=[feet_id])
    left_hand = relationship(
        "Item", foreign_keys=[left_hand_id])
    right_hand = relationship(
        "Item", foreign_keys=[right_hand_id])
    companion = relationship(
        "Item", foreign_keys=[companion_id])


engine = create_engine("sqlite:///InventoryCategories.db")
Base.metadata.create_all(engine)

