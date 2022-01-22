from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Administrator(Base):
    __tablename__ = 'administrators'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)

    user = relationship('User', backref=backref("administrators", uselist=False, passive_deletes=True))

    def __repr__(self):
        return f'Administrator(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, ' \
               f'user_id={self.user_id})'

    def __str__(self):
        return f'Administrator[id={self.id}, first_name={self.first_name}, last_name={self.last_name}, ' \
               f'user_id={self.user_id}]'
