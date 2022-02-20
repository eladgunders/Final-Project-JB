from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(Text(), unique=True, nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(Text(), unique=True, nullable=False)
    user_role = Column(Integer(), ForeignKey('user_roles.id'), nullable=False)

    role = relationship('User_Role', backref=backref("users", uselist=True))

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, password={self.password}, email={self.email}, ' \
               f'user_role={self.user_role})'

    def __str__(self):
        return f'User[id={self.id}, username={self.username}, password={self.password}, email={self.email}, ' \
               f'user_role={self.user_role}]'