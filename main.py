from datetime import datetime
from sqlalchemy import text
from db_config import local_session, create_all_entities
from Flight import Flight
from Country import Country
from Ticket import Ticket
from Airline_Company import Airline_Company
from Customer import Customer
from User import User
from User_Role import User_Role
from Administrator import Administrator
from AnonymousFacade import AnonymousFacade
from DbRepo import DbRepo


repo = DbRepo(local_session)

create_all_entities()  # create tables if not exist

