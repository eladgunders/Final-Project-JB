from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flights.id'), nullable=False, unique=True)
    customer_id = Column(BigInteger(), ForeignKey('customers.id'), nullable=False, unique=True)

    #__table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='una_1'),)  # one customer can buy only one ticket

    flight = relationship("Flight", backref=backref("tickets", uselist=False))
    customer = relationship("Customer", backref=backref("tickets", uselist=False))

    def __repr__(self):
        return f'Ticket(id={Ticket.id}, flight_id={Ticket.flight_id}, customer_id={Ticket.customer_id})'

    def __str__(self):
        return f'Ticket[id={Ticket.id}, flight_id={Ticket.flight_id}, customer_id={Ticket.customer_id}]'