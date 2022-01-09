from FacadeBase import FacadeBase
from Flight import Flight
from Airline_Company import Airline_Company
from Country import Country
from datetime import datetime, timedelta
from NotLegalFlightTimesError import NotLegalFlightTimesError


class AirlineFacade(FacadeBase):

    def __init__(self):
        super().__init__()

    def get_flights_by_airline(self, airline_id):
        if not isinstance(airline_id, int):
            print('Function failed, airline_id must be an integer.')
            return
        if airline_id <= 0:
            print('Function failed, airline_id must be positive.')
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
        if flight.departure_time + timedelta(hours=1) < flight.landing_time:  # checking the delta t
            print('Function failed, the delta t must be more than 1 hour.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            print('Function failed, remaining tickets must be an instance of the class int.')
            return
        if flight.remaining_tickets < 100:
            print('Function failed, remaining tickets must be 100 or more.')
            return
        if hasattr(flight, 'id'):
            delattr(flight, 'id')
            self.repo.add(flight)
        else:
            self.repo.add(flight)

    def update_airline(self, airline, id_):
        if not isinstance(id_, int):
            print('Function failed, id_ must be an integer.')
            return
        if id_ <= 0:
            print('Function failed, id_ must be greater than 0.')
            return


    def update_flight(self, flight, id_):
        pass
