from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, Text, ForeignKey, Boolean, Float, Enum
import enum

from ..database import Base
from sqlalchemy.orm import relationship



class Inventory(Base):
    __tablename__ = "inventory"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    money = Column("money", Float, default=200)
    wood = Column("wood", Float, default=200)
    wheat = Column("wheat", Float, default=200)
    skins = Column("skins", Float, default=200)
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
    user = relationship("User", back_populates='knights')



class Archer(Base):
    __tablename__ = "archer"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    attack = Column("attack", Integer)
    defense = Column("defense", Integer)
    agility = Column("agility", Integer)
    hp = Column("hp", Integer)
    max_hp = Column("max_hp", Integer)
    user = relationship("User", back_populates='archers')



class Citizen(Base):
    __tablename__ = "citizen"


    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))

    attack = Column("attack", Integer)
    defense = Column("defense", Integer)
    agility = Column("agility", Integer)

    hp = Column("hp", Integer)
    max_hp = Column("max_hp", Integer)
    user = relationship("User", back_populates='citizens')



class WoodHouse(Base):
    __tablename__ = "wood_house"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    res_per_worker = Column("res_per_worker", Float, default=1)

    workers = Column("workers", Integer, default=0)
    user = relationship("User", back_populates='wood_house')



class Fields(Base):
    __tablename__ = "fields"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    res_per_worker = Column("res_per_worker", Float, default=1)

    workers = Column("workers", Integer, default=0)
    user = relationship("User", back_populates='fields')



class HunterHouse(Base):
    __tablename__ = "hunter_house"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    res_per_worker = Column("res_per_worker", Float, default=1)

    workers = Column("workers", Integer, default=0)
    user = relationship("User", back_populates='hunter_house')



class TownSquare(Base):
    __tablename__ = "town_square"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)
    city_name = Column("city_name", String, default=None, nullable=True)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    wheat_for_next_lvl = Column("wheat_for_next_lvl", Integer, default=10)
    wood_for_next_lvl = Column("wood_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    time_for_citizen = Column("time_for_citizen", Integer, default=30)
    money_per_citizen = Column("money_per_citizen", Float, default=1)


    citizens_in_city = Column("citizens_in_city", Integer, default=0)
    unemployed_citizens = Column("unemployed_citizens", Integer, default=0)
    max_citizens = Column("max_citizens", Integer, default=150)
    user = relationship("User", back_populates='town_square')


class WarHouse(Base):
    __tablename__ = "war_house"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    skins_for_next_lvl = Column("skins_for_next_lvl", Integer, default=10)
    wood_for_next_lvl = Column("wood_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    time_for_knight = Column("time_for_knight", Integer, default=30)
    knights = Column("knights", Integer, default=0)
    max_knights = Column("max_knights", Integer, default=50)
    user = relationship("User", back_populates='war_house')


class Bar(Base):
    __tablename__ = "bar"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    skins_for_next_lvl = Column("skins_for_next_lvl", Integer, default=10)
    wood_for_next_lvl = Column("wood_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    time_for_archer = Column("time_for_archer", Integer, default=30)
    archers = Column("archers", Integer, default=0)
    max_archers = Column("max_archers", Integer, default=50)
    user = relationship("User", back_populates='bar')


class Market(Base):
    __tablename__ = "market"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    skins_for_next_lvl = Column("skins_for_next_lvl", Integer, default=10)
    wood_for_next_lvl = Column("wood_for_next_lvl", Integer, default=10)
    wheat_for_next_lvl = Column("wheat_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    taxes = Column("taxes", Float, default=15)
    user = relationship("User", back_populates='market')


class Tower(Base):
    __tablename__ = "tower"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"))
    cur_level = Column("cur_level", Integer, default=1)

    money_for_next_lvl = Column("money_for_next_lvl", Integer, default=10)
    wood_for_next_lvl = Column("wood_for_next_lvl", Integer, default=10)
    time_for_next_lvl = Column("time_for_next_lvl", Integer, default=30)

    user = relationship("User", back_populates='tower')


# user = User.__table__
# alembic revision --autogenerate -m 'INPUTMESSAGEHERE'
# alembic upgrade head
