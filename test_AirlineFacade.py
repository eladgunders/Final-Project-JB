import pytest
from AirlineFacade import AirlineFacade
from Flight import Flight
from datetime import datetime
from Airline_Company import Airline_Company
from NotLegalFlightTimesError import NotLegalFlightTimesError


@pytest.fixture(scope='session')
def dao_connection_singleton():
    print('Setting up same DAO for all tests.')
    return AirlineFacade()


@pytest.fixture(autouse=True)
def reset_db(dao_connection_singleton):
    dao_connection_singleton.repo.reset_test_db()
    return


@pytest.mark.parametrize('airline_id, expected', [('not int', None),
                                                  (0, None),
                                                  (7, None),
                                                  (1, [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200)])])
def test_airline_facade_get_flights_by_airline(dao_connection_singleton, airline_id, expected):
    actual = dao_connection_singleton.get_flights_by_airline_id(airline_id)
    assert actual == expected


@pytest.mark.parametrize('flight, expected', [('not flight', None),
                                              (Flight(airline_company_id=3, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=3, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=3,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime', remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100.7), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=99), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 21, 0, 0), remaining_tickets=100), True)])
def test_airline_facade_add_flight(dao_connection_singleton, flight, expected):
    actual = dao_connection_singleton.add_flight(flight)
    assert actual == expected


def test_airline_facade_add_flight_raise_notlegalflighttimeserror(dao_connection_singleton):
    with pytest.raises(NotLegalFlightTimesError):
        dao_connection_singleton.add_flight(Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 59, 0), remaining_tickets=100))


@pytest.mark.parametrize('airline, expected', [('not airline', None),
                                               (Airline_Company(id=3.3, name='Yoni', country_id=1, user_id=3), None),
                                               (Airline_Company(id=0, name='Yoni', country_id=1, user_id=3), None),
                                               (Airline_Company(id=3, name='Yoni', country_id=1, user_id=3), None),
                                               (Airline_Company(id=1, name='Yishay', country_id=1, user_id=3), None),
                                               (Airline_Company(id=1, name='Yishay', country_id=3, user_id=3), None),
                                               (Airline_Company(id=1, name='Yoniiii', country_id=2, user_id=3), True)])
def test_airline_facade_update_airline(dao_connection_singleton, airline, expected):
    actual = dao_connection_singleton.update_airline(airline)
    assert actual == expected


@pytest.mark.parametrize('flight, expected', [('not flight', None),
                                              (Flight(airline_company_id=3, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=3, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=3,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime', remaining_tickets=200), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100.7), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=-2), None),
                                              (Flight(id=3, airline_company_id=1, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), None),
                                              (Flight(id=1, airline_company_id=1, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), True)])
def test_airline_facade_update_flight(dao_connection_singleton, flight, expected):
    actual = dao_connection_singleton.update_flight(flight)
    assert actual == expected


def test_airline_facade_update_flight_raise_notlegalflighttimeserror(dao_connection_singleton):
    with pytest.raises(NotLegalFlightTimesError):
        dao_connection_singleton.update_flight(Flight(id=2, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 59, 0), remaining_tickets=100))