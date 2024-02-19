from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from ..database import Base



class User(Base):
    __tablename__ = "User"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String, nullable=False)
    username = Column("username", String, nullable=False)
    hashed_password = Column("hashed_password", String, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)



# user = User.__table__