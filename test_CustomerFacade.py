import pytest
from CustomerFacade import CustomerFacade
from Customer import Customer
from Ticket import Ticket
from NoRemainingTicketsError import NoRemainingTicketsError


@pytest.fixture(scope='session')
def dao_connection_singleton():
    print('Setting up same DAO for all tests.')
    return CustomerFacade()


@pytest.fixture(autouse=True)
def reset_db(dao_connection_singleton):
    dao_connection_singleton.repo.reset_test_db()
    return


@pytest.mark.parametrize('customer, expected', [('not customer', None),
                                                (Customer(id=1.1, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1), None),
                                                (Customer(id=0, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1), None),
                                                (Customer(id=3, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1), None),
                                                (Customer(id=2, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1), None),
                                                (Customer(id=2, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557000', credit_card_no='0000', user_id=1), None),
                                                (Customer(id=2, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557000', credit_card_no='9999', user_id=1), True)])
def test_customer_facade_update_customer(dao_connection_singleton, customer, expected):
    actual = dao_connection_singleton.update_customer(customer)
    assert actual == expected


@pytest.mark.parametrize('ticket, expected', [('not ticket', None),
                                              (Ticket(flight_id=3, customer_id=1), None),
                                              (Ticket(flight_id=1, customer_id=1), True)])
def test_customer_facade_remove_ticket(dao_connection_singleton, ticket, expected):
    actual = dao_connection_singleton.remove_ticket(ticket)
    assert actual == expected


@pytest.mark.parametrize('id_, expected', [('not int', None),
                                           (-1, None),
                                           (3, None),
                                           (1, [Ticket(id=1, flight_id=1, customer_id=1)])])
def test_customer_facade_get_tickets_by_customer(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_tickets_by_customer(id_)
    assert actual == expected


def test_customer_facade_add_ticket_raise_noremainingticketserror(dao_connection_singleton):
    with pytest.raises(NoRemainingTicketsError):
        dao_connection_singleton.add_ticket(Ticket(flight_id=2, customer_id=1))


@pytest.mark.parametrize('ticket, expected', [('not ticket', None),
                                              (Ticket(flight_id=4, customer_id=1), None),
                                              (Ticket(flight_id=1, customer_id=9), None),
                                              (Ticket(flight_id=1, customer_id=1), None),
                                              (Ticket(flight_id=1, customer_id=2), True)])
def test_customer_facade_add_ticket(dao_connection_singleton, ticket, expected):
    actual = dao_connection_singleton.add_ticket(ticket)
    assert actual == expected