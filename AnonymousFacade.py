from FacadeBase import FacadeBase
from CustomerFacade import CustomerFacade
from AirlineFacade import AirlineFacade
from AdministratorFacade import AdministratorFacade
from User import User
from Customer import Customer


class AnonymousFacade(FacadeBase):

    def __init__(self):
        super().__init__()

    def login(self, username, pw):
        user = self.repo.get_by_condition(User, lambda query: query.filter(User.username == username, User.password == pw).all())
        if not user:
            print('Function failed, user not found in the db.')
            return
        else:
            if user[0].user_role == 1:
                return CustomerFacade()
            elif user[0].user_role == 2:
                return AirlineFacade()
            elif user[0].user_role == 3:
                return AdministratorFacade()

    def add_customer(self, user, customer):
        if not isinstance(user, User):
            print('Function failed, user must be an instance of the class User.')
            return
        if user.user_role != 1:
            print('Function failed, user role must be 1(Customer).')
            return
        if self.create_user(user):
            if not isinstance(customer, Customer):
                print('Function failed. customer Must be an instance of the class Customer.')
                return
            if self.repo.get_by_condition(Customer,
                                          lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
                print('Function failed. a customer with this phone number already exists.')
                return
            if self.repo.get_by_condition(Customer,
                                          lambda query: query.filter(
                                              Customer.credit_card_no == customer.credit_card_no).all()):
                print('Function failed. a customer with this credit card number already exists.')
                return
            customer.id = None
            customer.user_id = user.id
            self.repo.add(customer)
            return True
        else:
            print('Function failed, user is not valid.')
            return