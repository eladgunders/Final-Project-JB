import pytest
from facades.AnonymousFacade import AnonymousFacade
from facades.CustomerFacade import CustomerFacade
from facades.AirlineFacade import AirlineFacade
from facades.AdministratorFacade import AdministratorFacade
from custom_errors.UserRoleTableError import UserRoleTableError
from custom_errors.WrongLoginDataError import WrongLoginDataError
from data_access_objects.DbRepoPool import DbRepoPool


@pytest.fixture(scope='session')
def anonymous_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    return AnonymousFacade(repo)


@pytest.fixture(autouse=True)
def reset_db(anonymous_facade_object):
    anonymous_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('username, password, expected', [('Elad', '123', CustomerFacade),
                                                          ('Yoni', '123', AirlineFacade),
                                                          ('Boris', '123', AdministratorFacade)])
def test_anonymous_facade_log_in(anonymous_facade_object, username, password, expected):
    actual = anonymous_facade_object.login(username, password)
    if expected is None:
        assert actual == expected
    else:
        assert isinstance(actual, expected)


def test_anonymous_facade_log_in_raise_wronglogindataerror(anonymous_facade_object):
    with pytest.raises(WrongLoginDataError):
        anonymous_facade_object.login('hh', '123')


def test_anonymous_facade_log_in_raise_userroletableerror(anonymous_facade_object):
    with pytest.raises(UserRoleTableError):
        anonymous_facade_object.login('not legal', '123')
