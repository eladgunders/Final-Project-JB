from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from db_config import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flights.id'), nullable=False)
    customer_id = Column(BigInteger(), ForeignKey('customers.id'), nullable=False)

    def __repr__(self):
        return f'Ticket(id={Ticket.id}, flight_id={Ticket.flight_id}, customer_id={Ticket.customer_id})'

    def __str__(self):
        return f'Ticket[id={Ticket.id}, flight_id={Ticket.flight_id}, customer_id={Ticket.customer_id}]'