from abc import ABC, abstractmethod
from datetime import datetime
from Flight import Flight
from DbRepo import DbRepo
from db_config import local_session
from Airline_Company import Airline_Company
from Country import Country
from User import User
from User_Role import User_Role
from sqlalchemy import extract


class FacadeBase(ABC):

    @abstractmethod
    def __init__(self):
        self.repo = DbRepo(local_session)

    def get_all_flights(self):
        return self.repo.get_all(Flight)

    def get_flight_by_id(self, id_):
        if not isinstance(id_, int):
            print('Function failed, id must be an integer.')
            return
        if id_ <= 0:
            print('Function failed, id must be positive.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == id_).all())

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        if not isinstance(origin_country_id, int) or not isinstance(destination_country_id, int):
            print('Function failed, both ids must be integers')
            return
        if origin_country_id <= 0 or destination_country_id <= 0:
            print('Function failed, both ids must be positive.')
            return
        if not isinstance(date, datetime):
            print('Function failed, date must be a datetime object.')
            return
        return self.repo.get_by_condition(Flight,
                                          lambda query: query.filter(Flight.origin_country_id == origin_country_id,
                                                                     Flight.destination_country_id == destination_country_id,
                                                                     extract('year', Flight.departure_time) == date.year,
                                                                     extract('month', Flight.departure_time) == date.month,
                                                                     extract('day', Flight.departure_time) == date.day).all())

    def get_all_airlines(self):
        return self.repo.get_all(Airline_Company)

    def get_airline_by_id(self, id_):
        if not isinstance(id_, int):
            print('Function failed, id must be an integer.')
            return
        if id_ <= 0:
            print('Function failed, id must be positive.')
            return
        return self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == id_).all())

    def create_user(self, user):
        if not isinstance(user, User):
            print('Function failed, user must be an instance of the class User.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.username == user.username).all()):
            print('Function failed, a user with the same username is already exists in the db.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.email == user.email).all()):
            print('Function failed, a user with the same email is already exists in the db.')
            return
        if not self.repo.get_by_condition(User_Role, lambda query: query.filter(User_Role.id == user.user_role).all()):
            print('Function failed, user_role does not exist in the user_roles table.')
            return
        user.id = None
        self.repo.add(user)
        return True

    def get_all_countries(self):
        return self.repo.get_all(Country)

    def get_country_by_id(self, id_):
        if not isinstance(id_, int):
            print('Function failed, id must be an integer.')
            return
        if id_ <= 0:
            print('Function failed, id must be positive.')
            return
        return self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == id_).all())

