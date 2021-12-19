from datetime import datetime
from sqlalchemy import text
from db_config import local_session, create_all_entities
from DbRepo import DbRepo
from Flight import Flight
from Country import Country
from Ticket import Ticket
from Airline_Company import Airline_Company
from Customer import Customer
from User import User
from User_Role import User_Role
from Administrator import Administrator
import sys


repo = DbRepo(local_session)  # creating a 'DAO'

create_all_entities()  # create tables if not exist

# adding rows to tables
'''
# flights
flight1 = Flight(airline_company_id=1, origin_country_id=1,
                 destination_country_id=1, departure_time=datetime.now(),
                 landing_time=datetime.utcnow(), remaining_tickets=23)
flight2 = Flight(airline_company_id=2, origin_country_id=2,
                 destination_country_id=2, departure_time=datetime.now(),
                 landing_time=datetime.utcnow(), remaining_tickets=7)
repo.add_all([flight1, flight2])

# countries
country1 = Country(name='Israel')
country2 = Country(name='Russia')
repo.add_all([country1, country2])

# tickets
ticket1 = Ticket(flight_id=1, customer_id=2)
ticket2 = Ticket(flight_id=2, customer_id=2)
repo.add_all([ticket1, ticket2])

# airline_companies
airline_company1 = Airline_Company(name='ElAl', country_id=1, user_id=1)
airline_company2 = Airline_Company(name='Lufthansa', country_id=2, user_id=2)
repo.add_all([airline_company1, airline_company2])

# customers
customer1 = Customer(first_name='Elad', last_name='Gunders', address='Sokolov 11',
                     phone_no='0545557007', credit_card_no='0000000000000000', user_id=1)
customer2 = Customer(first_name='Uri', last_name='Goldshmid', address='Helsinki 16',
                     phone_no='0527588331', credit_card_no='1111111111111111', user_id=2)
repo.add_all([customer1, customer2])

# users
user1 = User(username='Moishe', password='Moishe123', email='moishe@jb.com', user_role=1)
user2 = User(username='Ufnik', password='Ufnik123', email='ufnik@jb.com', user_role=2)
repo.add_all([user1, user2])

# user_roles
user_role1 = User_Role(role_name='Customer')
user_role2 = User_Role(role_name='Airline Company')
user_role3 = User_Role(role_name='Administrator')
repo.add_all([user_role1, user_role2, user_role3])

# Administrators
administrator1 = Administrator(first_name='Admin', last_name='One', user_id=1)
administrator2 = Administrator(first_name='Admin', last_name='Two', user_id=2)
repo.add_all([administrator1, administrator2])
'''
