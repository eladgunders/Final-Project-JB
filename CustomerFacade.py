from FacadeBase import FacadeBase
from Flight import Flight
from Customer import Customer
from Ticket import Ticket
from NoRemainingTicketsError import NoRemainingTicketsError


class CustomerFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token

    def update_customer(self, customer):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_customer but his role is not Customer.')
            return
        if not isinstance(customer, Customer):
            self.logger.logger.error(
                f'The login token "{self.login_token}" sent to the function customer :"{customer}" update_customer '
                f'but its not a Customer object.')
            return
        updated_customer = self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.id == self.login_token.id).all())
        if not updated_customer:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function update_customer but his customer_id not '
                f'exists in the db.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()) and \
                self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()) != updated_customer:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function update_customer but the phone number "{customer.phone_no}" '
                f'already exists in the db.')
            return
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.credit_card_no == customer.credit_card_no).all()) and \
                self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.credit_card_no == customer.credit_card_no).all()) != updated_customer:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function update_customer but the credit card number "{customer.credit_card_no}" '
                f'already exists in the db.')
            return
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function update_customer and updated to "{customer}"')
        self.repo.update_by_id(Customer, Customer.id, self.login_token.id, {Customer.first_name: customer.first_name, Customer.last_name: customer.last_name,
                                                                    Customer.address: customer.address, Customer.phone_no: customer.phone_no,
                                                                    Customer.credit_card_no: customer.credit_card_no})
        return True

    def add_ticket(self, ticket):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_ticket but his role is not Customer.')
            return
        if not isinstance(ticket, Ticket):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_ticket but the ticket "{ticket}" '
                f'that was sent to the function is not a Ticket object.')
            return
        flight = self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.id == ticket.flight_id).all())
        if not flight:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_ticket but the flight.id "{ticket.flight_id}" '
                f'that was sent to the function not exists in the db.')
            return
        if flight[0].remaining_tickets <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_ticket but the flight has no remaining tickets')
            raise NoRemainingTicketsError
        if self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == self.login_token.id,
                                                                         Ticket.flight_id == ticket.flight_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_ticket but this customer already has a ticket for this flight')
            return
        self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,  # updating the remaining tickets of the flight
                               {Flight.remaining_tickets: flight[0].remaining_tickets - 1})
        ticket.id = None
        ticket.customer_id = self.login_token.id
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function add_ticket and added this ticket "{ticket}"')
        self.repo.add(ticket)
        return True

    def remove_ticket(self, ticket):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_ticket but his role is not Customer.')
            return
        if not isinstance(ticket, Ticket):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_ticket but the ticket "{ticket}" '
                f'that was sent is not a Ticket object.')
            return
        ticket_ = self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.flight_id == ticket.flight_id,
                                                                               Ticket.customer_id == self.login_token.id).all())
        if not ticket_:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_ticket but the ticket "{ticket}" '
                f'that was sent not exist in the db.')
            return
        if ticket_[0].customer_id != self.login_token.id:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_ticket but the ticket.customer_id "{ticket.customer_id}" '
                f'is not belong to the login_token.')
            return
        self.repo.update_by_id(Flight, Flight.id, ticket_[0].flight.id,
                               {Flight.remaining_tickets: ticket_[0].flight.remaining_tickets + 1})
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_ticket and removed the ticket "{ticket}"')
        self.repo.delete_by_id(Ticket, Ticket.id, ticket_[0].id)
        return True

    def get_tickets_by_customer(self):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function get_tickets_by_customer but his role is not Customer.')
            return
        return self.repo.get_by_condition(Ticket, lambda query: query.filter(Ticket.customer_id == self.login_token.id).all())



