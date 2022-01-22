from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Airline_Company(Base):
    __tablename__ = 'airline_companies'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), unique=True, nullable=False)
    country_id = Column(BigInteger(), ForeignKey('countries.id'), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)

    user = relationship('User', backref=backref("airline_companies", uselist=False, passive_deletes=True))

    def __eq__(self, other):
        if isinstance(other, Airline_Company):
            return self.id == other.id and self.name == other.name and \
                   self.country_id == other.country_id and self.user_id == other.user_id
        else:
            return False

    def __repr__(self):
        return f'Airline_Company(id={Airline_Company.id}, name={Airline_Company.name}' \
               f', country_id={Airline_Company.country_id}, user_id={Airline_Company.user_id})'

    def __str__(self):
        return f'Airline_Company[id={Airline_Company.id}, name={Airline_Company.name}' \
               f', country_id={Airline_Company.country_id}, user_id={Airline_Company.user_id}]'