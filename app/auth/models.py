from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from ..database import Base
from sqlalchemy.orm import relationship, Mapped
from app.levels.models import *


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String, nullable=False)
    username = Column("username", String, nullable=False)
    hashed_password = Column("hashed_password", String, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    inventory: Mapped[Inventory] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    messages: Mapped[List[Message]] = relationship(back_populates="user")

    knights: Mapped[List[Knight]] = relationship(back_populates="user")
    archers: Mapped[List[Archer]] = relationship(back_populates="user")
    citizens: Mapped[List[Citizen]] = relationship(back_populates="user")
    wood_house: Mapped[WoodHouse] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    fields: Mapped[Fields] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    hunter_house: Mapped[HunterHouse] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    town_square: Mapped[TownSquare] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    war_house: Mapped[WarHouse] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    bar: Mapped[Bar] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    market: Mapped[Market] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)
    tower: Mapped[Tower] = relationship(back_populates='user', cascade='all,delete-orphan', single_parent=True)



    def __str__(self):
        return f"Пользователь №{self.id} ебать"



# user = User.__table__
# alembic revision --autogenerate -m 'INPUTMESSAGEHERE'
# alembic upgrade head
