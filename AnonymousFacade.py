from FacadeBase import FacadeBase
from User import User
from User_Role import User_Role


class AnonymousFacade(FacadeBase):

    def __init__(self):
        super().__init__()

    def login(self, username, pw):
        if not self.repo.get_by_condition(User, lambda query: query.filter(User.username == username).all()):  # what happens if finds 2 usernames?
            print('Function failed, wrong username.')
            return False
        if not self.repo.get_by_condition(User, lambda query: query.filter(User.password == pw).all()):
            print('Function failed, wrong password.')
            return False
        return True

    def create_user(self, user):
        if not isinstance(user, User):
            print('Function failed, user must be an instance of the class User.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.username == user.username).all()):
            print('Function failed, a user with the same username is already exists in the db.')
            return
        if self.repo.get_by_condition(User, lambda query: query.filter(User.email == user.email).all()):
            print('Function failed, a user with the same email is already exists in the db.')
            return
        if not self.repo.get_by_condition(User_Role, lambda query: query.filter(User_Role.id == user.user_role).all()):
            print('Function failed, user_role does not exist in the user_roles table.')
        self.repo.add(user)
