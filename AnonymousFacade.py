from FacadeBase import FacadeBase
from CustomerFacade import CustomerFacade
from AirlineFacade import AirlineFacade
from AdministratorFacade import AdministratorFacade
from User import User
from Customer import Customer
from LoginToken import LoginToken
from UserRoleTableError import UserRoleTableError


class AnonymousFacade(FacadeBase):

    facade_dic = {1: lambda login_token, repo: CustomerFacade(login_token, repo), 2: lambda login_token, repo: AirlineFacade(login_token, repo),
                  3: lambda login_token, repo: AdministratorFacade(login_token, repo)}

    def __init__(self, repo):
        self.repo = repo
        super().__init__(self.repo)

    def login(self, username, pw):
        user = self.repo.get_by_condition(User, lambda query: query.filter(User.username == username, User.password == pw).all())
        if not user:
            self.logger.logger.info(
                f'Wrong username {username} or password {pw} has been entered to the login function.')
            return
        else:
            if user[0].user_role == 1:
                token_dic = {'id': user[0].customers.id, 'name': user[0].customers.first_name, 'role': 'Customer'}
            elif user[0].user_role == 2:
                token_dic = {'id': user[0].airline_companies.id, 'name': user[0].airline_companies.name, 'role': 'Airline_Company'}
            elif user[0].user_role == 3:
                token_dic = {'id': user[0].administrators.id, 'name': user[0].administrators.first_name, 'role': 'Administrator'}
            else:
                self.logger.logger.error(
                    f'User Roles table contains more than 3 user roles. Please check it ASAP.')
                raise UserRoleTableError

            login_token = LoginToken(token_dic['id'], token_dic['name'],
                                     token_dic['role'])

            self.logger.logger.debug(f'{login_token} logged in to the system.')
            return AnonymousFacade.facade_dic[user[0].user_role](login_token, self.repo)

    def add_customer(self, user, customer):
        if not isinstance(user, User):
            self.logger.logger.error(f'the user "{user}" that was sent to the function add_customer is not a User instance.')
            return
        if user.user_role != 1:
            self.logger.logger.error(f'the user.user_role "{user.user_role}" is not 1(Customer).')
            return
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
        if self.create_user(user):
            customer.id = None
            customer.user_id = user.id
            self.logger.logger.debug(f'A Customer "{customer}" connected by the User "{user}" has been added to the db.')
            self.repo.add(customer)
            return True
        else:
            self.logger.logger.error(f'The function add_customer failed - the User "{user} "that was sent is not valid.')
            return