from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, Text, ForeignKey, Boolean, Float

from ..database import Base
from sqlalchemy.orm import relationship



class Inventory(Base):
    __tablename__ = "inventory"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    money = Column("money", Integer, default=0)
    wood = Column("wood", Integer, default=0)
    wheat = Column("wheat", Integer, default=0)
    skins = Column("skins", Integer, default=0)
    user = relationship("User", back_populates='inventory')



class Knight(Base):
    __tablename__ = "knight"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    attack = Column("attack", Integer)
    defense = Column("defense", Integer)
    agility = Column("agility", Integer)
    hp = Column("hp", Integer)
    max_hp = Column("max_hp", Integer)
    user = relationship("User", back_populates='knight')



class Archer(Base):
    __tablename__ = "archer"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    attack = Column("attack", Integer)
    defense = Column("defense", Integer)
    agility = Column("agility", Integer)
    hp = Column("hp", Integer)
    max_hp = Column("max_hp", Integer)
    user = relationship("User", back_populates='archer')


class Peasant(Base):
    __tablename__ = "peasant"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    attack = Column("attack", Integer)
    defense = Column("defense", Integer)
    agility = Column("agility", Integer)
    hp = Column("hp", Integer)
    on_duty = Column("on_duty", Boolean)
    max_hp = Column("max_hp", Integer)
    user = relationship("User", back_populates='peasant')


class WoodHouse(Base):
    __tablename__ = "wood_house"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)
    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=100)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=5)
    res_per_worker = Column("res_per_worker", Float, default=1)
    user = relationship("User", back_populates='wood_house')


class Fields(Base):
    __tablename__ = "fields"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)
    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=100)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=5)
    res_per_worker = Column("res_per_worker", Float, default=1)
    user = relationship("User", back_populates='fields')


class HunterHouse(Base):
    __tablename__ = "hunter_house"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)
    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=100)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=5)
    res_per_worker = Column("res_per_worker", Float, default=1)
    user = relationship("User", back_populates='hunter_house')

