from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from db_config import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    address = Column(Text(), nullable=False)
    phone_no = Column(Text(), nullable=False, unique=True)
    credit_card_no = Column(Text(), nullable=False, unique=True)
    user_id = Column(BigInteger(), ForeignKey('users.id'), unique=True)

    def __repr__(self):
        return f'Customer(id={Customer.id}, first_name={Customer.first_name}, last_name={Customer.last_name}, ' \
               f'address={Customer.address}, phone_no={Customer.phone_no}, credit_card_no={Customer.credit_card_no}, ' \
               f'user_id={Customer.user_id})'

    def __str__(self):
        return f'Customer[id={Customer.id}, first_name={Customer.first_name}, last_name={Customer.last_name}, ' \
               f'address={Customer.address}, phone_no={Customer.phone_no}, credit_card_no={Customer.credit_card_no}, ' \
               f'user_id={Customer.user_id}]'