from datetime import datetime
from FacadeBase import FacadeBase
from Flight import Flight
from DbRepo import DbRepo
from db_config import local_session
from Airline_Company import Airline_Company
from Country import Country
from Customer import Customer
from User import User
from User_Role import User_Role
from Ticket import Ticket
from NoRemainingTicketsError import NoRemainingTicketsError


class CustomerFacade(FacadeBase):

    def __init__(self):
        self.repo = DbRepo(local_session)

    def update_customer(self, customer, id_):
        if not isinstance(id_, int):
            print('Function failed, id must be an integer.')
            return
        if id_ <= 0:
            print('Function failed, id must be positive.')
            return
        if not self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.id == id_).all()):
            print('Function failed, a customer with this id does not exist.')
            return
        if not isinstance(customer, Customer):
            print('Function failed, customer must be an instance of the class Customer.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
            print('Function failed, a customer with this phone number is already exists.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.credit_card_no == customer.credit_card_no).all()):
            print('Function failed, a customer with this credit card number is already exists.')
            return
        if not self.repo.get_by_condition(User, lambda query: query.filter(User.id == customer.user_id).all()):
            print('Function failed, no such user with this id.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.user_id == customer.user_id).all()):
            print('Function failed, a customer with this user_id does already exist in the db.')
        customer.id = None
        self.repo.update_by_id(Customer, Customer.id, id_, customer.__dict__)

    def add_ticket(self, ticket):
        if not isinstance(ticket, Ticket):
            print('Function failed, ticket must be an instance of the class Ticket.')
            return
        flight = self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == ticket.flight_id).all())
        if not flight:
            print('Function failed, flight_id does not exist in flights table.')
            return
        elif flight[0].remaining_tickets <= 0:
            raise NoRemainingTicketsError(msg=f'User id: {ticket.customer.user_id} '
                                          f'tried to add this ticket but no tickets remaining')
        if not self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.id == ticket.customer_id).all()):
            print('Function failed, customer_id does not exist in customers table.')
            return
        if self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == ticket.customer_id,
                                                                         Ticket.flight_id == ticket.flight_id).all()):
            print('Function failed, this customer already have a ticket for this flight.')
            return
        self.repo.update_by_id(Flight, Flight.remaining_tickets, ticket.flight_id,  # updating the remaining tickets of the flight
                               {Flight.remaining_tickets: flight[0].remaining_tickets - 1})
        flight.id = None
        self.repo.add(ticket)

    def remove_ticket(self, id_):
        if not isinstance(id_, int):
            print('Function failed, id must be an integer.')
            return
        if id_ <= 0:
            print('Function failed, id must be positive.')
            return
        ticket = self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.id == id_).all())
        if not ticket:
            print('Function failed, no ticket with this id in the db.')
            return
        self.repo.update_by_id(Flight, Flight.id, ticket[0].flight.id,
                               {Flight.remaining_tickets: ticket[0].flight.remaining_tickets + 1})
        self.repo.delete_by_id(Ticket, Ticket.id, id_)

    def get_tickets_by_customer(self, customer_id):
        if not isinstance(customer_id, int):
            print('Function failed, customer_id must be an integer.')
            return
        if customer_id <= 0:
            print('Function failed, customer id must be positive.')
            return
        return self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == customer_id).all())



