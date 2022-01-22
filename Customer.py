from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref, foreign
from db_config import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    address = Column(Text(), nullable=False)
    phone_no = Column(Text(), nullable=False, unique=True)
    credit_card_no = Column(Text(), nullable=False, unique=True)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)

    user = relationship('User', backref=backref("customers", uselist=False, passive_deletes=True))

    def __eq__(self, other):
        if isinstance(other, Customer):
            return self.id == other.id and self.first_name == other.first_name and self.last_name == other.last_name and \
                   self.address == other.address and self.phone_no == other.phone_no and self.credit_card_no == other.credit_card_no and \
                   self.user_id == other.user_id
        else:
            return False

    def __repr__(self):
        return f'Customer(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, ' \
               f'address={self.address}, phone_no={self.phone_no}, credit_card_no={self.credit_card_no}, ' \
               f'user_id={self.user_id})'

    def __str__(self):
        return f'Customer[id={self.id}, first_name={self.first_name}, last_name={self.last_name}, ' \
               f'address={self.address}, phone_no={self.phone_no}, credit_card_no={self.credit_card_no}, ' \
               f'user_id={self.user_id}]'