from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from db_config import Base


class Administrator(Base):
    __tablename__ = 'administrators'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    user_id = Column(BigInteger(),ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Administrator(id={Administrator.id}, first_name={Administrator.first_name}, last_name={Administrator.last_name}, ' \
               f'user_id={Administrator.user_id})'

    def __str__(self):
        return f'Administrator[id={Administrator.id}, first_name={Administrator.first_name}, last_name={Administrator.last_name}, ' \
               f'user_id={Administrator.user_id}]'
