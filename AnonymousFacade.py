from FacadeBase import FacadeBase
from CustomerFacade import CustomerFacade
from AirlineFacade import AirlineFacade
from AdministratorFacade import AdministratorFacade
from User import User
from User_Role import User_Role


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