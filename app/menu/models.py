from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, Text

from ..database import Base



class Menu(Base):
    __tablename__ = "menu"

    id = Column("id", Integer, primary_key=True)
    slug = Column("slug", String)
    name = Column("name", String)
    img_link = Column("img_link", String)
    descr = Column("descr", Text)




