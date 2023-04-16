from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Bread(SqlAlchemyBase):
    __tablename__ = 'bread'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    short = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    img = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("bread_type.id"), nullable=False)
    type = relationship('Btype')
