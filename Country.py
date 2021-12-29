from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, REAL, Text
from sqlalchemy.orm import relationship
from db_config import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(Text(), unique=True, nullable=False)

    def __repr__(self):
        return f'Country(id={Country.id}, name={Country.name})'

    def __str__(self):
        return f'Country[id={Country.id}, name={Country.name}]'