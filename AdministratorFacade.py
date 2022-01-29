from FacadeBase import FacadeBase
from Customer import Customer
from User import User
from Flight import Flight
from Ticket import Ticket
from Airline_Company import Airline_Company
from Administrator import Administrator
from Country import Country
from Logger import Logger


class AdministratorFacade(FacadeBase):

    def __init__(self, login_token):
        self.login_token = login_token
        self.logger = Logger.get_instance()
        super().__init__()

    def get_all_customers(self):
        if self.login_token.role != 'Administrator':
            print('Function failed, login_token in not Administrator.')
            return
        return self.repo.get_all(Customer)

    def add_administrator(self, user, administrator):
        if self.login_token.role != 'Administrator':
            print('Function failed, login_token in not Administrator.')
            return
        if not isinstance(user, User):
            print('Function failed, user must be an instance of the class User.')
            return
        if user.user_role != 3:
            print('Function failed, user role must be 1(Customer).')
            return
        if self.create_user(user):
            if not isinstance(administrator, Administrator):
                print('Function failed. customer Must be an instance of the class Customer.')
                return
            administrator.id = None
            administrator.user_id = user.id
            self.repo.add(administrator)
            return True
        else:
            print('Function failed, user is not valid.')
            return

    def remove_administrator(self, administrator_id):
        if self.login_token.role != 'Administrator':
            print('Function failed, login_token in not Administrator.')
            return
        if not isinstance(administrator_id, int):
            print('Function failed customer_id must be an integer.')
            return
        if administrator_id <= 0:
            print('Function failed, customer_id must be positive.')
            return
        admin = self.repo.get_by_condition(Administrator, lambda query: query.filter(Administrator.id == administrator_id).all())
        if not admin:
            print('Function failed, no such administrator in the db, wrong administrator id.')
            return
        self.repo.delete_by_id(User, User.id, admin[0].user.id)
        return True

    def remove_airline(self, airline_id):
        if self.login_token.role != 'Administrator':
            print('Function failed, login_token in not Administrator.')
            return
        if not isinstance(airline_id, int):
            print('Function failed, id must be an integer.')
            return
        if airline_id <= 0:
            print('Function failed, id must be positive.')
            return
        airline = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == airline_id).all())
        if not airline:
            print('Function failed, no such Airline Company in the db. wrong airline_id.')
            return
        self.repo.delete_by_id(User, User.id, airline[0].user.id)
        return True

    def remove_customer(self, customer_id):
        if self.login_token.role != 'Administrator':
            print('Function failed, login_token in not Administrator.')
            return
        if not isinstance(customer_id, int):
            print('Function failed, customer_id must be an integer.')
            return
        if customer_id <= 0:
            print('Function failed, customer_id must be positive.')
            return
        customer = self.repo.get_by_condition(Customer,
                                           lambda query: query.filter(Customer.id == customer_id).all())
        if not customer:
            print('Function failed, no such customer in the db. wrong customer_id.')
            return
        tickets = self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == customer_id).all())
        for ticket in tickets:
            self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,  # updating the remaining tickets of the flight
                                   {Flight.remaining_tickets: ticket.flight.remaining_tickets + 1})
        self.repo.delete_by_id(User, User.id, customer[0].user.id)
        return True

    def add_customer(self, user, customer):
        if not isinstance(user, User):
            self.logger.logger.error(
                f'the user "{user}" that was sent to the function add_customer is not a User instance.')
            return
        if user.user_role != 1:
            self.logger.logger.error(f'the user.user_role "{user.user_role}" is not 1(Customer).')
            return
        if self.create_user(user):
            if not isinstance(customer, Customer):
                self.logger.logger.error(
                    f'the customer "{customer}" that was sent to the function add_customer is not a Customer instance.')
                return
            if self.repo.get_by_condition(Customer,
                                          lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
                self.logger.logger.error(
                    f'the customer.phone_no "{customer.phone_no}" that was sent the function add_customer is already exists in the db.')
                return
            if self.repo.get_by_condition(Customer,
                                          lambda query: query.filter(
                                              Customer.credit_card_no == customer.credit_card_no).all()):
                self.logger.logger.error(
                    f'the customer.credit_card_no "{customer.credit_card_no}" that was sent the function add_customer is already exists in the db.')
                return
            customer.id = None
            customer.user_id = user.id
            self.logger.logger.debug(f'A Customer "{customer}" connected by the User "{user}" has been added to the db.')
            self.repo.add(customer)
            return True
        else:
            self.logger.logger.error(f'The function add_customer failed - the User "{user}" that was sent is not valid.')
            return

    def add_airline(self, user, airline):
        if self.login_token.role != 'Administrator':
            print('Function failed, login_token in not Administrator.')
            return
        if not isinstance(user, User):
            print('Function failed, user must be an instance of the class User.')
            return
        if user.user_role != 2:
            print('Function failed, user role must be 2(Airline Company).')
            return
        if self.create_user(user):
            if not isinstance(airline, Airline_Company):
                print('Function failed. airline Must be an instance of the class Airline_Company.')
                return
            if self.repo.get_by_condition(Airline_Company,
                                          lambda query: query.filter(Airline_Company.name == airline.name).all()):
                print('Function failed. An Airline with this name already exists.')
                return
            if not self.repo.get_by_condition(Country,
                                          lambda query: query.filter(Country.id == airline.country_id).all()):
                print('Function failed, airline.country_id does not exist in the db.')
                return
            airline.id = None
            airline.user_id = user.id
            self.repo.add(airline)
            return True
        else:
            print('Function failed, user is not valid.')
            return