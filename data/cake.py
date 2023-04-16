from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Cake(SqlAlchemyBase):
    __tablename__ = 'cake'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    short = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    img = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("cake_type.id"), nullable=False)
    type = relationship('Ctype')

    def __repr__(self):
        return f'<{self.__tablename__}> id: {self.id} title: {self.title}'

