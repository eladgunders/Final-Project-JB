from FacadeBase import FacadeBase
from Customer import Customer
from User import User
from Flight import Flight
from Ticket import Ticket
from Airline_Company import Airline_Company
from Administrator import Administrator
from Country import Country


class AdministratorFacade(FacadeBase):

    def __init__(self, login_token):
        self.login_token = login_token
        super().__init__()

    def get_all_customers(self):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function get_all_customers but his role is '
                f'not Administrator.')
            return
        return self.repo.get_all(Customer)

    def add_administrator(self, user, administrator):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but his role is '
                f'not Administrator.')
            return
        if not isinstance(user, User):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but the user "{user}" '
                f'that was sent is not a User object.')
            return
        if user.user_role != 3:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but the user.user_role "{user.user_role}" '
                f'that was sent is not 3(Administrator).')
            return
        if self.create_user(user):
            if not isinstance(administrator, Administrator):
                self.logger.logger.error(
                    f'The login token "{self.login_token}" tried to use the function add_administrator but the administrator "{administrator}" '
                    f'that was sent is not an Administrator object.')
                return
            administrator.id = None
            administrator.user_id = user.id
            self.logger.logger.debug(
                f'The login token "{self.login_token}" used the function add_administrator and added administrator "{administrator}" '
                f'that connected to the user "{user}".')
            self.repo.add(administrator)
            return True
        else:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but the user "{user}" '
                f'that was sent is not valid so the function failed.')
            return

    def remove_administrator(self, administrator_id):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but his role is '
                f'not Administrator.')
            return
        if not isinstance(administrator_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                f'that was sent is not an integer.')
            return
        if administrator_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                f'that was sent is not positive.')
            return
        admin = self.repo.get_by_condition(Administrator, lambda query: query.filter(Administrator.id == administrator_id).all())
        if not admin:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                f'that was sent does not exist in the db.')
            return
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_administrator and removed the administrator "{admin}"')
        self.repo.delete_by_id(User, User.id, admin[0].user.id)
        return True

    def remove_airline(self, airline_id):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but his role is '
                f'not Administrator.')
            return
        if not isinstance(airline_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                f'that was sent is not an integer.')
            return
        if airline_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                f'that was sent is not an positive.')
            return
        airline = self.repo.get_by_condition(Airline_Company, lambda query: query.filter(Airline_Company.id == airline_id).all())
        if not airline:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                f'that was sent does not exist in the db.')
            return
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_airline and removed the airline "{airline}"')
        self.repo.delete_by_id(User, User.id, airline[0].user.id)
        return True

    def remove_customer(self, customer_id):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but his role is '
                f'not Administrator.')
            return
        if not isinstance(customer_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent is not an integer.')
            return
        if customer_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent is not positive.')
            return
        customer = self.repo.get_by_condition(Customer,
                                           lambda query: query.filter(Customer.id == customer_id).all())
        if not customer:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent does not exist in the db.')
            return
        tickets = self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == customer_id).all())
        for ticket in tickets:
            self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,  # updating the remaining tickets of the flight
                                   {Flight.remaining_tickets: ticket.flight.remaining_tickets + 1})
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_customer and removed the customer "{customer}"')
        self.repo.delete_by_id(User, User.id, customer[0].user.id)
        return True

    def add_customer(self, user, customer):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but his role is '
                f'not Administrator.')
        if not isinstance(user, User):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but user "{user}" '
                f'that was sent is not a User instance.')
            return
        if user.user_role != 1:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but the user.user_role "{user.user_role}" '
                f'that was sent is not 1(Customer).')
            return
        if self.create_user(user):
            if not isinstance(customer, Customer):
                self.logger.logger.error(
                    f'The login token "{self.login_token}" tried to use the function add_customer but customer "{customer}" '
                    f'that was sent is not a Customer object.')
                return
            if self.repo.get_by_condition(Customer,
                                          lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
                self.logger.logger.error(
                    f'The login token "{self.login_token}" tried to use the function add_customer but customer.phone_no "{customer.phone_no}" '
                    f'that was sent already exists in the db.')
                return
            if self.repo.get_by_condition(Customer,
                                          lambda query: query.filter(
                                              Customer.credit_card_no == customer.credit_card_no).all()):
                self.logger.logger.error(
                    f'The login token "{self.login_token}" tried to use the function add_customer but customer.credit_card_no "{customer.credit_card_no}" '
                    f'that was sent already exists in the db.')
                return
            customer.id = None
            customer.user_id = user.id
            self.logger.logger.debug(
                f'The login token "{self.login_token}" used the function add_customer and added the customer "{customer}" '
                f'connected by the user "{user}".')
            self.repo.add(customer)
            return True
        else:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but the user "{user}" '
                f'that was sent is not valid so the function failed.')
            return

    def add_airline(self, user, airline):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but his role is '
                f'not Administrator.')
            return
        if not isinstance(user, User):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but user "{user}" '
                f'that was sent is not a User object.')
            return
        if user.user_role != 2:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but the user.user_role "{user.user_role}" '
                f'that was sent is not 2(Airline).')
            return
        if self.create_user(user):
            if not isinstance(airline, Airline_Company):
                self.logger.logger.error(
                    f'The login token "{self.login_token}" tried to use the function add_airline but airline "{airline}" '
                    f'that was sent is not an Airline Company object.')
                return
            if self.repo.get_by_condition(Airline_Company,
                                          lambda query: query.filter(Airline_Company.name == airline.name).all()):
                self.logger.logger.error(
                    f'The login token "{self.login_token}" tried to use the function add_airline but airline.name "{airline.name}" '
                    f'that was sent already exists in the db.')
                return
            if not self.repo.get_by_condition(Country,
                                          lambda query: query.filter(Country.id == airline.country_id).all()):
                self.logger.logger.error(
                    f'The login token "{self.login_token}" tried to use the function add_airline but airline.country_id "{airline.country_id}" '
                    f'that was sent does not exist in the db.')
                return
            airline.id = None
            airline.user_id = user.id
            self.logger.logger.debug(
                f'The login token "{self.login_token}" used the function add_airline and added airline "{airline}" '
                f'that connected to the user "{user}".')
            self.repo.add(airline)
            return True
        else:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but the user "{user}" '
                f'that was sent is not valid so the function failed.')
            return