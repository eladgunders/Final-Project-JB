from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger
from sqlalchemy.orm import relationship
from db_config import Base


class User_Role(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    role_name = Column(Text(), unique=True, nullable=False)

    def __repr__(self):
        return f'User_Role(id={User_Role.id}, role_name={User_Role.role_name})'

    def __str__(self):
        return f'User_Role[id={User_Role.id}, role_name={User_Role.role_name}]'