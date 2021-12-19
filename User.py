from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger
from sqlalchemy.orm import relationship
from db_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(Text(), unique=True, nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(Text(), unique=True, nullable=False)
    user_role = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'User(id={User.id}, username={User.username}, password={User.password}, email={User.email}, ' \
               f'user_role={User.user_role})'

    def __str__(self):
        return f'User[id={User.id}, username={User.username}, password={User.password}, email={User.email}, ' \
               f'user_role={User.user_role}]'