import pytest
from facades.AnonymousFacade import AnonymousFacade
from tables.User import User
from tables.Administrator import Administrator
from tables.Customer import Customer
from tables.Airline_Company import Airline_Company
from custom_errors.NotValidDataError import NotValidDataError
from data_access_objects.DbRepoPool import DbRepoPool


@pytest.fixture(scope='session')
def administrator_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('Boris', '123')


@pytest.fixture(autouse=True)
def reset_db(administrator_facade_object):
    administrator_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('user, administrator, expected', [(User(username='Eladi', password='123', email='eladi@gmail.com', user_role=3),
                                                            Administrator(first_name='Borissss', last_name='Boriiii', user_id=6), True)])
def test_administrator_facade_add_administrator(administrator_facade_object, user, administrator, expected):
    actual = administrator_facade_object.add_administrator(user, administrator)
    assert actual == expected


@pytest.mark.parametrize('user, administrator', [('not user', 2),
                                                 (User(username='Elad', password='123', email='elad@gmail.com', user_role=9), 2),
                                                 (User(username='Elad', password='123', email='elad@gmail.com', user_role=3), 2),
                                                 (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=3), 'k')])
def test_administrator_facade_add_administrator_raise_notvaliddataerror(administrator_facade_object, user, administrator):
    with pytest.raises(NotValidDataError):
        administrator_facade_object.add_administrator(user, administrator)


def test_administrator_facade_get_all_customers(administrator_facade_object):
    actual = administrator_facade_object.get_all_customers()
    expected = [Customer(id=1, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1),
                Customer(id=2, first_name='Uri', last_name='Goldshmid', address='Helsinki 16',
                         phone_no='0527588331', credit_card_no='0001', user_id=2)]
    assert actual == expected


@pytest.mark.parametrize('admin_id, expected', [(1, True)])
def test_administrator_facade_remove_administrator(administrator_facade_object, admin_id, expected):
    actual = administrator_facade_object.remove_administrator(admin_id)
    assert actual == expected


@pytest.mark.parametrize('admin_id', ['not int', -1, 3])
def test_administrator_facade_remove_administrator_raise_notvaliddataerror(administrator_facade_object, admin_id):
    with pytest.raises(NotValidDataError):
        administrator_facade_object.remove_administrator(admin_id)


@pytest.mark.parametrize('customer_id, expected', [(1, True), (2, True)])
def test_administrator_facade_remove_customer(administrator_facade_object, customer_id, expected):
    actual = administrator_facade_object.remove_customer(customer_id)
    assert actual == expected


@pytest.mark.parametrize('customer_id', ['f', 0, 3])
def test_administrator_facade_remove_customer_raise_notvaliddataerror(administrator_facade_object, customer_id):
    with pytest.raises(NotValidDataError):
        administrator_facade_object.remove_customer(customer_id)


@pytest.mark.parametrize('airline_id, expected', [(1, True)])
def test_administrator_facade_remove_airline(administrator_facade_object, airline_id, expected):
    actual = administrator_facade_object.remove_airline(airline_id)
    assert actual == expected


@pytest.mark.parametrize('airline_id', ['f', -1, 4])
def test_administrator_facade_remove_airline_raise_notvaliddataerror(administrator_facade_object, airline_id):
    with pytest.raises(NotValidDataError):
        administrator_facade_object.remove_airline(airline_id)


@pytest.mark.parametrize('user, customer, expected', [
                                                      (User(username='Elados', password='123', email='eladii@gmail.com', user_role=1),
                                                       Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                        phone_no='0545557004', credit_card_no='0055', user_id=8) , True)
                                                      ])
def test_administrator_facade_add_customer(administrator_facade_object, user, customer, expected):
    actual = administrator_facade_object.add_customer(user, customer)
    assert actual == expected


@pytest.mark.parametrize('user, customer', [(1, 1),
                                            (
                                            User(username='Elad', password='123', email='eladi@gmail.com', user_role=2),
                                            Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                     phone_no='0545557000', credit_card_no='0099', user_id=1)),
                                            (User(username='Elados', password='123', email='eladi@gmail.coom',
                                                  user_role=2),
                                             Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                      phone_no='0545557000', credit_card_no='0099', user_id=1)),
                                                (User(username='Elad', password='123', email='eladi@gmail.com',
                                                      user_role=1),
                                                 Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                          phone_no='0545557000', credit_card_no='0099', user_id=1)),
                                                (User(username='Elados', password='123', email='eladi@gmail.coom',
                                                      user_role=2), 'g'),
                                            (User(username='Elados', password='123', email='eladii@gmail.com',
                                                 user_role=1),
                                            Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                     phone_no='0545557007', credit_card_no='0099', user_id=1)),
                                            (User(username='Elados', password='123', email='eladii@gmail.com',
                                                  user_role=1),
                                             Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                      phone_no='0545557004', credit_card_no='0000', user_id=1))])
def test_administrator_facade_add_customer_raise_notvaliddataerror(administrator_facade_object, user, customer):
    with pytest.raises(NotValidDataError):
        administrator_facade_object.add_customer(user, customer)


@pytest.mark.parametrize('user, airline, expected', [
                                                     (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2),
                                                      Airline_Company(name='Yonchkin', country_id=1, user_id=8), True)])
def test_administrator_facade_add_airline(administrator_facade_object, user, airline, expected):
    actual = administrator_facade_object.add_airline(user, airline)
    assert actual == expected


@pytest.mark.parametrize('user, airline', [(1, 1),
                                           (User(username='Elad', password='123', email='eladi@gmail.com', user_role=1), 1),
                                           (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2), 1),
                                           (
                                           User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2),
                                           Airline_Company(name='Yoni', country_id=1, user_id=3)),
                                           (
                                           User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2),
                                           Airline_Company(name='Yonchkin', country_id=3, user_id=3))])
def test_administrator_facade_add_airline_raise_notvaliddataerror(administrator_facade_object, user, airline):
    with pytest.raises(NotValidDataError):
        administrator_facade_object.add_customer(user, airline)