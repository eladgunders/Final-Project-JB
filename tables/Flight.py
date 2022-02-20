from sqlalchemy import Column, Integer, String, DateTime, REAL, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id', ondelete='CASCADE'), nullable=False)
    origin_country_id = Column(BigInteger(), ForeignKey('countries.id'), nullable=False)
    destination_country_id = Column(BigInteger(), ForeignKey('countries.id'), nullable=False)
    departure_time = Column(DateTime(), nullable=False)
    landing_time = Column(DateTime(), nullable=False)
    remaining_tickets = Column(Integer(), nullable=False)

    airline_company = relationship('Airline_Company', backref=backref("flights", uselist=True, passive_deletes=True))
    origin_county = relationship('Country', foreign_keys=[origin_country_id], backref=backref("oc_flights", uselist=True))
    destination_county = relationship('Country', foreign_keys=[destination_country_id], backref=backref("dc_flights", uselist=True))

    def __eq__(self, other):
        if isinstance(other, Flight):
            return self.id == other.id and self.airline_company_id == other.airline_company_id and \
                   self.origin_country_id == other.origin_country_id and \
                   self.destination_country_id == other.destination_country_id and \
                   self.departure_time == other.departure_time and self.landing_time == other.landing_time and \
                   self.remaining_tickets == other.remaining_tickets
        else:
            return False

    def __repr__(self):
        return f'Flight(id={self.id}, airline_company_id={self.airline_company_id}, origin_country_id={self.origin_country_id}, ' \
               f'destination_country_id={self.destination_country_id}, departure_time={self.departure_time}, landing_time={self.landing_time}, ' \
               f'remaining_tickets={self.remaining_tickets})'

    def __str__(self):
        return f'Flight[id={self.id}, airline_company_id={self.airline_company_id}, origin_country_id={self.origin_country_id}, ' \
               f'destination_country_id={self.destination_country_id}, departure_time={self.departure_time}, landing_time={self.landing_time}, ' \
               f'remaining_tickets={self.remaining_tickets}]'
    