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
from Logger import Logger


class FacadeBase(ABC):

    @abstractmethod
    def __init__(self):
        self.logger = Logger.get_instance()
        self.repo = DbRepo(local_session)

    def get_all_flights(self):
        return self.repo.get_all(Flight)

    def get_flight_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'the id "{id_}" that was sent to the function get_flight_by_id is not an integer.')
            return
        if id_ <= 0:
            self.logger.logger.error(
                f'the id "{id_}" that was sent to the function get_flight_by_id is not positive.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == id_).all())

    def get_flights_by_airline_id(self, airline_id):
        if not isinstance(airline_id, int):
            self.logger.logger.error(
                f'the airline_id "{airline_id}" that was sent to the function get_flight_by_airline_id is not an integer.')
            return
        if airline_id <= 0:
            self.logger.logger.error(
                f'the airline_id "{airline_id}" that was sent to the function get_flight_by_airline_id is not positive.')
            return
        air_line_ = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == airline_id).all())
        if not air_line_:
            self.logger.logger.error(
                f'the airline_id "{airline_id}" that was sent to the function get_flight_by_airline_id is exists in the db.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.airline_company_id == airline_id).all())

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        if not isinstance(origin_country_id, int) or not isinstance(destination_country_id, int):
            self.logger.logger.error(
                f'the county ids "{origin_country_id}" and "{destination_country_id}" '
                f'that was sent to the function get_flight_by_parameters must be integers')
            return
        if origin_country_id <= 0 or destination_country_id <= 0:
            self.logger.logger.error(
                f'the county ids "{origin_country_id}" and "{destination_country_id}" '
                f'that was sent to the function get_flight_by_parameters must be positive')
            return
        if not isinstance(date, datetime):
            self.logger.logger.error(
                f'the the date "{date}" that was sent to the function get_flight_by_parameters must be a Datetime object')
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
            self.logger.logger.error(
                f'the id "{id_}" that was sent to the function get_airline_by_id is not an integer.')
            return
        if id_ <= 0:
            self.logger.logger.error(
                f'the id "{id_}" that was sent to the function get_airline_by_id is not positive.')
            return
        return self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == id_).all())

    def create_user(self, user):
        if not isinstance(user, User):
            self.logger.logger.error(
                f'The user "{user}" that was sent to the function create_user must be instance if the class User.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.username == user.username).all()):
            self.logger.logger.error(
                f'The user.username "{user.username}" that was sent to the function create_user already exists in the db.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.email == user.email).all()):
            self.logger.logger.error(
                f'The user.email "{user.email}" that was sent to the function create_user already exists in the db.')
            return
        if not self.repo.get_by_condition(User_Role, lambda query: query.filter(User_Role.id == user.user_role).all()):
            self.logger.logger.error(
                f'The user.user.user_role "{user.user_role}" that was sent to the function create_user not exists in the user_roles table.')
            return
        user.id = None
        self.logger.logger.debug(f'new user "{user}" has ben added to the db.')
        self.repo.add(user)
        return True

    def get_all_countries(self):
        return self.repo.get_all(Country)

    def get_country_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'the id "{id_}" that was sent to the function get_country_by_id is not an integer.')
            return
        if id_ <= 0:
            self.logger.logger.error(
                f'the id "{id_}" that was sent to the function get_country_by_id is not positive.')
            return
        return self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == id_).all())

