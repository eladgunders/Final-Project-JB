import pytest
from facades.AnonymousFacade import AnonymousFacade
from tables.Flight import Flight
from datetime import datetime
from tables.Airline_Company import Airline_Company
from custom_errors.NotLegalFlightTimesError import NotLegalFlightTimesError
from custom_errors.NoRemainingTicketsError import NoRemainingTicketsError
from custom_errors.WrongLoginTokenError import WrongLoginTokenError
from custom_errors.NotValidDataError import NotValidDataError
from data_access_objects.DbRepoPool import DbRepoPool


@pytest.fixture(scope='session')
def airline_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('Yoni', '123')


@pytest.fixture(autouse=True)
def reset_db(airline_facade_object):
    airline_facade_object.repo.reset_test_db()
    return


def test_airline_facade_get_airline_flights(airline_facade_object):
    actual = airline_facade_object.get_airline_flights()
    assert actual == [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                             departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200)]


@pytest.mark.parametrize('flight, expected', [
                                              (Flight(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 21, 0, 0), remaining_tickets=100), True)])
def test_airline_facade_add_flight(airline_facade_object, flight, expected):
    actual = airline_facade_object.add_flight(flight)
    assert actual == expected


@pytest.mark.parametrize('flight', ['not flight',
                                    Flight(origin_country_id=3, destination_country_id=2,
                                           departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                           landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200),
                                    Flight(origin_country_id=1, destination_country_id=3,
                                            departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                            remaining_tickets=200),
                                    Flight(origin_country_id=1, destination_country_id=2,
                                            departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200),
                                    Flight(origin_country_id=1, destination_country_id=2,
                                            departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime', remaining_tickets=200),
                                    Flight(origin_country_id=1, destination_country_id=2,
                                            departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                            remaining_tickets=100.7),
                                    Flight(origin_country_id=1, destination_country_id=2,
                                            departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                            remaining_tickets=99)])
def test_airline_facade_add_flight_raise_notvaliddataerror(airline_facade_object, flight):
    with pytest.raises(NotValidDataError):
        airline_facade_object.add_flight(flight)


def test_airline_facade_add_flight_raise_notlegalflighttimeserror(airline_facade_object):
    with pytest.raises(NotLegalFlightTimesError):
        airline_facade_object.add_flight(Flight(origin_country_id=1, destination_country_id=2,
                                                departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 59, 0), remaining_tickets=100))


@pytest.mark.parametrize('airline, expected', [(Airline_Company(name='Yoniiiiii', country_id=2, user_id=3), True)])
def test_airline_facade_update_airline(airline_facade_object, airline, expected):
    actual = airline_facade_object.update_airline(airline)
    assert actual == expected


@pytest.mark.parametrize('airline', ['not airline',
                                     Airline_Company(name='Yishay', country_id=1, user_id=3),
                                     Airline_Company(name='Yoni', country_id=3, user_id=3)])
def test_airline_facade_update_airline_raise_notvaliddataerror(airline_facade_object, airline):
    with pytest.raises(NotValidDataError):
        airline_facade_object.update_airline(airline)


@pytest.mark.parametrize('flight, expected', [(Flight(id=1, airline_company_id=1, origin_country_id=2,
                                                      destination_country_id=1,
                                                      departure_time=datetime(2022, 1, 29, 17, 0, 0),
                                                      landing_time=datetime(2022, 1, 30, 14, 0, 0),
                                                      remaining_tickets=0), True)])
def test_airline_facade_update_flight(airline_facade_object, flight, expected):
    actual = airline_facade_object.update_flight(flight)
    assert actual == expected


@pytest.mark.parametrize('flight', ['not flight',
                                    Flight(airline_company_id=3, origin_country_id=1, destination_country_id=2,
                                           departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                           landing_time=datetime(2022, 1, 30, 20, 0, 0)),
                                    Flight(airline_company_id=1, origin_country_id=3, destination_country_id=2,
                                           departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                           landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200),
                                    Flight(airline_company_id=1, origin_country_id=1, destination_country_id=3,
                                           departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                           landing_time=datetime(2022, 1, 30, 20, 0, 0)),
                                    Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                           departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                           remaining_tickets=200),
                                    Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                           departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime',
                                           remaining_tickets=200),
                                    Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                           departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                           landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100.7),
                                    Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                           departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                           landing_time=datetime(2022, 1, 30, 20, 0, 0)),
                                    Flight(id=3, airline_company_id=1, origin_country_id=2, destination_country_id=1,
                                           departure_time=datetime(2022, 1, 29, 17, 0, 0),
                                           landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0)])
def test_airline_facade_update_flight_raise_notvaliddataerror(airline_facade_object, flight):
    with pytest.raises(NotValidDataError):
        airline_facade_object.update_flight(flight)


def test_airline_facade_update_flight_raise_wrongloginlokenerror(airline_facade_object):
    with pytest.raises(WrongLoginTokenError):
        airline_facade_object.update_flight(Flight(id=2, airline_company_id=2, origin_country_id=2,
                                                   destination_country_id=1,
                                                   departure_time=datetime(2022, 1, 29, 17, 0, 0),
                                                   landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0))


def test_airline_facade_update_flight_raise_notlegalflighttimeserror(airline_facade_object):
    with pytest.raises(NotLegalFlightTimesError):
        airline_facade_object.update_flight(Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                                   departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 59, 0), remaining_tickets=100))


def test_airline_facade_update_flight_raise_noremainingticketserror(airline_facade_object):
    with pytest.raises(NoRemainingTicketsError):
        airline_facade_object.update_flight(Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                                   departure_time=datetime(2022, 1, 29, 00, 0, 0),
                                                   landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=-5))


@pytest.mark.parametrize('flight_id, expected', [(1, True)])
def test_airline_facade_remove_flight(airline_facade_object, flight_id, expected):
    actual = airline_facade_object.remove_flight(flight_id)
    assert actual == expected


@pytest.mark.parametrize('flight_id', ['not_id', 0, 4])
def test_airline_facade_remove_flight_raise_notvaliddataerror(airline_facade_object, flight_id):
    with pytest.raises(NotValidDataError):
        airline_facade_object.remove_flight(flight_id)


def test_airline_facade_remove_flight_raise_wronglogintokenerror(airline_facade_object):
    with pytest.raises(WrongLoginTokenError):
        airline_facade_object.remove_flight(2)