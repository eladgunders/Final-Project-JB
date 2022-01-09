from sqlalchemy import asc, text, desc
from Customer import Customer
from Administrator import Administrator
from Airline_Company import Airline_Company
from Country import Country
from Flight import Flight
from Ticket import Ticket
from User_Role import User_Role
from User import User
from datetime import datetime


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def reset_auto_inc(self, table_class):
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
        self.local_session.commit()

    def get_all(self, table_class):
        return self.local_session.query(table_class).all()

    def get_all_limit(self, table_class, limit_num):
        return self.local_session.query(table_class).limit(limit_num).all()

    def get_all_order_by(self, table_class, column_name, direction=asc):
        return self.local_session.query(table_class).order_by(direction(column_name)).all()

    def get_by_column_value(self, table_class, column_value, value):
        return self.local_session.query(table_class).filter(column_value == value).all()

    def get_by_condition(self, table_class, condition):  # condition is a lambda expression of a filter
        return condition(self.local_session.query(table_class))

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def delete_by_id(self, table_class, id_column_name, id_):
        self.local_session.query(table_class).filter(id_column_name == id_).delete(synchronize_session=False)
        self.local_session.commit()

    def update_by_id(self, table_class, id_column_name, id_, data):  # data is a dictionary of all the new columns and values
        self.local_session.query(table_class).filter(id_column_name == id_).update(data)
        self.local_session.commit()

    def drop_all_tables(self):
        self.local_session.execute('DROP TABLE users CASCADE')
        self.local_session.execute('DROP TABLE user_roles CASCADE')
        self.local_session.execute('DROP TABLE tickets CASCADE')
        self.local_session.execute('DROP TABLE flights CASCADE')
        self.local_session.execute('DROP TABLE customers CASCADE')
        self.local_session.execute('DROP TABLE countries CASCADE')
        self.local_session.execute('DROP TABLE airline_companies CASCADE')
        self.local_session.execute('DROP TABLE administrators CASCADE')
        self.local_session.commit()

    def reset_test_db(self):
        # resetting auto increment for all tables
        self.reset_auto_inc(Country)
        self.reset_auto_inc(User_Role)
        self.reset_auto_inc(User)
        self.reset_auto_inc(Administrator)
        self.reset_auto_inc(Airline_Company)
        self.reset_auto_inc(Customer)
        self.reset_auto_inc(Flight)
        self.reset_auto_inc(Ticket)
        # county
        israel = Country(name='Israel')
        self.add(israel)
        self.add(Country(name='Germany'))
        # user role
        self.add(User_Role(role_name='Customer'))
        self.add(User_Role(role_name='Airline Company'))
        self.add(User_Role(role_name='Administrator'))
        # user
        self.add(User(username='Elad', password='123', email='elad@gmail.com', user_role=1))
        self.add(User(username='Uri', password='123', email='uri@gmail.com', user_role=1))
        self.add(User(username='Yoni', password='123', email='yoni@gmail.com', user_role=2))
        self.add(User(username='Yishay', password='123', email='yishay@gmail.com', user_role=2))
        self.add(User(username='Tomer', password='123', email='tomer@gmail.com', user_role=3))
        self.add(User(username='Boris', password='123', email='boris@gmail.com', user_role=3))
        # administrator
        self.add(Administrator(first_name='Tomer', last_name='Tome', user_id=5))
        self.add(Administrator(first_name='Boris', last_name='Bori', user_id=6))
        # airline company
        self.add(Airline_Company(name='Yoni', country_id=1, user_id=3))
        self.add(Airline_Company(name='Yishay', country_id=2, user_id=4))
        # customer
        self.add(Customer(first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1))
        self.add(Customer(first_name='Uri', last_name='Goldshmid', address='Helsinki 16',
                          phone_no='0527588331', credit_card_no='0001', user_id=2))
        # flight
        self.add(Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0),
                        landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200))
        self.add(Flight(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0),
                        landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200))
        # ticket
        self.add(Ticket(flight_id=1, customer_id=1))
        self.add(Ticket(flight_id=2, customer_id=2))


