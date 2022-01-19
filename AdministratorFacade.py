from FacadeBase import FacadeBase
from Customer import Customer
from User import User
from Administrator import Administrator


class AdministratorFacade(FacadeBase):

    def __init__(self):
        super().__init__()

    def get_all_customers(self):
        return self.repo.get_all(Customer)

    def add_administrator(self, user, administrator):
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
        pass

    def remove_customer(self, customer_id):  # needs to add to remaining tickets all the tickets this customer has
        customer = self.repo.get_by_condition(Customer,
                                           lambda query: query.filter(Customer.id == customer_id).all())
        self.repo.delete_by_id(User, User.id, customer[0].user.id)
        return True