from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from ..database import Base
from sqlalchemy.orm import relationship, Mapped


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String, nullable=False)
    username = Column("username", String, nullable=False)
    hashed_password = Column("hashed_password", String, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    inventory = relationship("Inventory", back_populates='user', cascade='all,delete-orphan', single_parent=True)
    knights = relationship("Knight", back_populates='user')
    archers = relationship("Archer", back_populates='user')
    peasants = relationship("Peasant", back_populates='user')
    wood_house = relationship("WoodHouse", back_populates='user', cascade='all,delete-orphan', single_parent=True)
    fields = relationship("Fields", back_populates='user', cascade='all,delete-orphan', single_parent=True)
    hunter_house = relationship("HunterHouse", back_populates='user', cascade='all,delete-orphan', single_parent=True)



# user = User.__table__
# alembic revision --autogenerate -m 'INPUTMESSAGEHERE'
# alembic upgrade head
