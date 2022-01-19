from FacadeBase import FacadeBase
from Flight import Flight
from Airline_Company import Airline_Company
from Country import Country
from datetime import datetime, timedelta
from NotLegalFlightTimesError import NotLegalFlightTimesError


class AirlineFacade(FacadeBase):

    def __init__(self):
        super().__init__()

    def get_flights_by_airline_id(self, airline_id):
        if not isinstance(airline_id, int):
            print('Function failed, airline_id must be an integer.')
            return
        if airline_id <= 0:
            print('Function failed, airline_id must be positive.')
            return
        air_line_ = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == airline_id).all())
        if not air_line_:
            print('Function failed, no such airline in the db, id is wrong.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.airline_company_id == airline_id).all())

    def add_flight(self, flight):
        if not isinstance(flight, Flight):
            print('Function failed, flight must be an instance of the class Flight.')
            return
        if not self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == flight.airline_company_id).all()):
            print('Function failed, airline_company_id does not exist in airline_company table.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.origin_country_id).all()):
            print('Function failed, origin_country_id does not exist in countries table.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.destination_country_id).all()):
            print('Function failed, destination_country_id does not exist in countries table.')
            return
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            print('Function failed, departure_time and landing_time must be datetime objects.')
            return
        if flight.departure_time + timedelta(hours=1) > flight.landing_time:  # checking the delta t
            print('Function failed, the delta t must be more than 1 hour.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            print('Function failed, remaining tickets must be an instance of the class int.')
            return
        if flight.remaining_tickets < 100:
            print('Function failed, remaining tickets must be 100 or more.')
            return
        flight.id = None
        self.repo.add(flight)
        return True

    def update_airline(self, airline):
        if not isinstance(airline, Airline_Company):
            print('Function failed, airline must be an instance of the class Airline_Company')
            return
        if not isinstance(airline.id, int):
            print('Function failed, airline.id must be an integer.')
            return
        if airline.id <= 0:
            print('Function failed, airline.id must be greater than 0.')
            return
        airline_ = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == airline.id).all())
        if not airline_:
            print('Function failed, no such airline in the db, wrong id.')
            return
        if self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.name == airline.name).all())\
                and self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.name == airline.name).all()) != airline_:
            print('Function failed, theres already an airline with this name.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == airline.country_id).all()):
            print('Function failed, no such country in the db. wrong airline.country_id')
            return
        self.repo.update_by_id(Airline_Company, Airline_Company.id, airline.id, {Airline_Company.name: airline.name,
                                                                                 Airline_Company.country_id: airline.country_id})
        return True

    def update_flight(self, flight):
        if not isinstance(flight, Flight):
            print('Function failed, flight must be an instance of the class Flight.')
            return
        if not isinstance(flight.id, int):
            print('Function failed, flight.id must be an integer.')
            return
        if flight.id <= 0:
            print('Function failed, flight.id must be positive.')
            return
        if not isinstance(flight.origin_country_id, int) or not isinstance(flight.destination_country_id, int):
            print('Function failed, both countries_id must be integers.')
            return
        if flight.origin_country_id <= 0 or flight.destination_country_id <= 0:
            print('Function failed, both country_id must be positive.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.origin_country_id).all()):
            print('Function failed, origin_country_id not found in the db.')
            return
        if not self.repo.get_by_condition(Country, lambda query: query.filter(Country.id == flight.destination_country_id).all()):
            print('Function failed, destination_country_id not found in the db.')
            return
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            print('Function failed, departure_time and landing_time must be datetime objects.')
            return
        if flight.departure_time + timedelta(hours=1) > flight.landing_time:  # checking the delta t
            print('Function failed, the delta t must be more than 1 hour.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            print('Function failed, remaining tickets must be an instance of the class int.')
            return
        if flight.remaining_tickets < 0:
            print('Function failed, remaining tickets must be 100 or more.')
            return
        flight_ = self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == flight.id).all())
        if not flight_:
            print('Function failed, flight not found in the db, wrong flight.id.')
            return
        self.repo.update_by_id(Flight, Flight.id, flight.id, {Flight.origin_country_id: flight.origin_country_id,
                                                              Flight.destination_country_id: flight.destination_country_id,
                                                              Flight.departure_time: flight.departure_time,
                                                              Flight.landing_time: flight.landing_time,
                                                              Flight.remaining_tickets: flight.remaining_tickets})
        return True

