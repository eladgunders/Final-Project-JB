import pytest
from AdministratorFacade import AdministratorFacade
from User import User
from Administrator import Administrator
from Customer import Customer
from Flight import Flight
from datetime import datetime
from Airline_Company import Airline_Company
from Ticket import Ticket


@pytest.fixture(scope='session')
def dao_connection_singleton():
    print('Setting up same DAO for all tests.')
    return AdministratorFacade()


@pytest.fixture(autouse=True)
def reset_db(dao_connection_singleton):
    dao_connection_singleton.repo.reset_test_db()
    return


@pytest.mark.parametrize('user, administrator, expected', [('not user', 2, None),
                                                           (User(username='Elad', password='123', email='elad@gmail.com', user_role=9), 2, None),
                                                           (User(username='Elad', password='123', email='elad@gmail.com', user_role=3), 2, None),
                                                           (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=3), 'k', None),
                                                           (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=3),
                                                            Administrator(first_name='Borissss', last_name='Boriiii', user_id=6), True)])
def test_administrator_facade_add_administrator(dao_connection_singleton, user, administrator, expected):
    actual = dao_connection_singleton.add_administrator(user, administrator)
    assert actual == expected


def test_administrator_facade_get_all_customers(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_customers()
    expected = [Customer(id=1, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1),
                Customer(id=2, first_name='Uri', last_name='Goldshmid', address='Helsinki 16',
                         phone_no='0527588331', credit_card_no='0001', user_id=2)]
    assert actual == expected


@pytest.mark.parametrize('admin_id, expected', [('not int', None),
                                                (-1, None),
                                                (3, None),
                                                (1, True)])
def test_administrator_facade_remove_administrator(dao_connection_singleton, admin_id, expected):
    actual = dao_connection_singleton.remove_administrator(admin_id)
    assert actual == expected


@pytest.mark.parametrize('customer_id, expected', [(1, True)])
def test_administrator_facade_remove_customer(dao_connection_singleton, customer_id, expected):
    actual = dao_connection_singleton.remove_customer(customer_id)
    assert actual == expected

