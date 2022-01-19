from FacadeBase import FacadeBase
from Flight import Flight
from DbRepo import DbRepo
from db_config import local_session
from Customer import Customer
from Ticket import Ticket
from NoRemainingTicketsError import NoRemainingTicketsError


class CustomerFacade(FacadeBase):

    def __init__(self):
        self.repo = DbRepo(local_session)

    def update_customer(self, customer):
        if not isinstance(customer, Customer):
            print('Function failed, customer must be an instance of the class Customer.')
            return
        if not isinstance(customer.id, int):
            print('Function failed, id must be an integer.')
            return
        if customer.id <= 0:
            print('Function failed, id must be positive.')
            return
        updated_customer = self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.id == customer.id).all())
        if not updated_customer:
            print('Function failed, a customer with this id does not exist.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()) and \
                self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()) != updated_customer:
            print('Function failed, a customer with this phone number is already exists.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.credit_card_no == customer.credit_card_no).all()) and \
                self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.credit_card_no == customer.credit_card_no).all()) != updated_customer:
            print('Function failed, a customer with this credit card number is already exists.')
            return
        self.repo.update_by_id(Customer, Customer.id, customer.id, {Customer.first_name: customer.first_name, Customer.last_name: customer.last_name,
                                                                    Customer.address: customer.address, Customer.phone_no: customer.phone_no,
                                                                    Customer.credit_card_no: customer.credit_card_no})
        return True

    def add_ticket(self, ticket):
        if not isinstance(ticket, Ticket):
            print('Function failed, ticket must be an instance of the class Ticket.')
            return
        flight = self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == ticket.flight_id).all())
        if not flight:
            print('Function failed, flight_id does not exist in flights table.')
            return
        if flight[0].remaining_tickets <= 0:
            raise NoRemainingTicketsError
        if not self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.id == ticket.customer_id).all()):
            print('Function failed, customer_id does not exist in customers table.')
            return
        if self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == ticket.customer_id,
                                                                         Ticket.flight_id == ticket.flight_id).all()):
            print('Function failed, this customer already have a ticket for this flight.')
            return
        self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,  # updating the remaining tickets of the flight
                               {Flight.remaining_tickets: flight[0].remaining_tickets - 1})
        ticket.id = None
        self.repo.add(ticket)
        return True

    def remove_ticket(self, ticket):
        if not isinstance(ticket, Ticket):
            print('Function failed, ticket must be an instance of the class Ticket.')
            return
        ticket_ = self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.flight_id == ticket.flight_id,
                                                                               Ticket.customer_id == ticket.customer_id).all())
        if not ticket_:
            print('Function failed, no such ticket in the db.')
            return
        self.repo.update_by_id(Flight, Flight.id, ticket_[0].flight.id,
                               {Flight.remaining_tickets: ticket_[0].flight.remaining_tickets + 1})
        self.repo.delete_by_id(Ticket, Ticket.id, ticket_[0].id)
        return True

    def get_tickets_by_customer(self, customer_id):
        if not isinstance(customer_id, int):
            print('Function failed, customer_id must be an integer.')
            return
        if customer_id <= 0:
            print('Function failed, customer id must be positive.')
            return
        customer_ = self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.id == customer_id).all())
        if not customer_:
            print('Function failed, wrong id, no such customer in the db.')
            return
        return self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == customer_id).all())



