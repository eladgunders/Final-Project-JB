from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id'), nullable=False)
    origin_country_id = Column(Integer(), ForeignKey('countries.id'), nullable=False)
    destination_country_id = Column(Integer(), ForeignKey('countries.id'), nullable=False)
    departure_time = Column(DateTime(), nullable=False)
    landing_time = Column(DateTime(), nullable=False)
    remaining_tickets = Column(Integer(), nullable=False)

    airline_company = relationship('Airline_Company', backref=backref("flights", uselist=True))
    origin_county = relationship('Country', backref=backref("flights", uselist=True))
    destination_county = relationship('Country', backref=backref("flights", uselist=True))

    def __repr__(self):
        return f'Flight(id={Flight.id}, airline_company_id={Flight.airline_company_id}, origin_country_id ={Flight.origin_country_id}, ' \
               f'destination_country_id={Flight.destination_country_id}, departure_time={Flight.departure_time}, landing_time={Flight.landing_time}, ' \
               f'remaining_tickets={Flight.remaining_tickets})'

    def __str__(self):
        return f'Flight[id={Flight.id}, airline_company_id={Flight.airline_company_id}, origin_country_id ={Flight.origin_country_id}, ' \
               f'destination_country_id={Flight.destination_country_id}, departure_time={Flight.departure_time}, landing_time={Flight.landing_time}, ' \
               f'remaining_tickets={Flight.remaining_tickets}]'
    