import pytest
from AnonymousFacade import AnonymousFacade
from CustomerFacade import CustomerFacade
from AirlineFacade import AirlineFacade
from AdministratorFacade import AdministratorFacade
from User import User


@pytest.fixture(scope='session')
def dao_connection_singleton():
    print('Setting up same DAO for all tests.')
    return AnonymousFacade()


@pytest.mark.parametrize('username, password, expected', [('Elad', '123', CustomerFacade),
                                                          ('Yoni', '123', AirlineFacade),
                                                          ('Boris', '123', AdministratorFacade),
                                                          ('hh', '123', None)])
def test_anonymous_facade_log_in(dao_connection_singleton, username, password, expected):
    actual = dao_connection_singleton.login(username, password)
    if expected is None:
        assert actual == expected
    else:
        assert isinstance(actual, expected)
