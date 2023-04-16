from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Btype(SqlAlchemyBase):
    __tablename__ = 'bread_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
