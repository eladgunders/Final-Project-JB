from abc import ABC, abstractmethod
from datetime import datetime
from Flight import Flight
from DbRepo import DbRepo
from db_config import local_session
from Airline_Company import Airline_Company
from Country import Country
from Customer import Customer
from User import User


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
                                                                     Flight.departure_time.year == date.year).all())

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

    def add_customer(self, customer):
        if not isinstance(customer, Customer):
            print('Function failed. customer Must be an instance of the class Customer.')
            return
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
            print('Function failed. a customer with this phone number already exists.')
            return
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(
                                          Customer.credit_card_no == customer.credit_card_no).all()):
            print('Function failed. a customer with this credit card number already exists.')
            return
        if not self.repo.get_by_condition(User,
                                          lambda query: query.filter(User.id == customer.user_id).all()):
            print('Function failed. no such User with this user_id.')
            return
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(Customer.user_id == customer.user_id).all()):
            print('Function failed. A customer with the same user_id is already exists.')
            return
        self.repo.add(customer)

    def add_airline(self, airline):
        if not isinstance(airline, Airline_Company):
            print('Function failed. airline Must be an instance of the class Airline_Company.')
            return
        if self.repo.get_by_condition(Airline_Company,
                                      lambda query: query.filter(Airline_Company.name == airline.name).all()):
            print('Function failed. An Airline with this name already exists.')
            return
        if not self.repo.get_by_condition(User,
                                          lambda query: query.filter(User.id == airline.user_id).all()):
            print('Function failed. no such User with this user_id.')
        if self.repo.get_by_condition(Airline_Company,
                                      lambda query: query.filter(Airline_Company.user_id == airline.user_id).all()):
            print('Function failed. An Airline with the same user_id is already exists.')
            return
        self.repo.add(airline)

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

