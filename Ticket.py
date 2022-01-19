from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flights.id'), nullable=False)
    customer_id = Column(BigInteger(), ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='una_1'),)  # customer can buy 1 ticket per flight

    flight = relationship("Flight", backref=backref("tickets", uselist=True))
    customer = relationship("Customer", backref=backref("tickets", uselist=True, passive_deletes=True))

    def __eq__(self, other):
        if isinstance(other, Ticket):
            return self.customer_id == other.customer_id and self.flight_id == other.flight_id
        else:
            return False

    def __repr__(self):
        return f'Ticket(id={Ticket.id}, flight_id={Ticket.flight_id}, customer_id={Ticket.customer_id})'

    def __str__(self):
        return f'Ticket[id={Ticket.id}, flight_id={Ticket.flight_id}, customer_id={Ticket.customer_id}]'