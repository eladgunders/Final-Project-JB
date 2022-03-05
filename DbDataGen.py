from tables.Customer import Customer
from tables.Country import Country
from tables.User import User
from tables.User_Role import User_Role
from tables.Flight import Flight
from tables.Ticket import Ticket
from tables.Administrator import Administrator
from tables.Airline_Company import Airline_Company
from data_access_objects.DbRepoPool import DbRepoPool
from logger.Logger import Logger
from datetime import timedelta
import random
import httpx
import json
import trio
from faker import Faker


class DbDataGen:

    customer_role = 1
    airline_role = 2
    admin_role = 3
    number_of_countries_in_db = None
    max_hours_delta_t = 15
    remaining_tickets_per_flight = 200

    def __init__(self, url):
        self.url = url
        self.repool = DbRepoPool.get_instance()
        self.repo = self.repool.get_connection()
        self.logger = Logger.get_instance()
        self.fake = Faker()

    @staticmethod
    def generate_credit_card_num():
        ccn = str(random.randint(0, 9))
        for i in range(11):
            ccn = ccn + str(random.randint(0, 9))
        return ccn

    async def get_data(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.url)
            return r.json()

    def generate_countries(self):
        countries_ls = []
        with open(r"db_generator\countries.json") as f:
            countries = json.load(f)
        for country in countries:
            countries_ls.append(Country(name=country['name']))
        self.repo.add_all(countries_ls)
        self.number_of_countries_in_db = len(countries_ls)

    def generate_user_roles(self):
        self.repo.add(User_Role(role_name='Customer'))
        self.repo.add(User_Role(role_name='Airline Company'))
        self.repo.add(User_Role(role_name='Administrator'))

    def create_user(self, j_son, user_role):
        username = j_son['results'][0]['login']['username']
        pw = j_son['results'][0]['login']['password']
        email = j_son['results'][0]['email']
        inserted_user = User(username=username, password=pw, email=email, user_role=user_role)
        self.repo.add(inserted_user)
        return inserted_user

    def generate_admin(self):
        data = trio.run(self.get_data)
        user = self.create_user(data, self.admin_role)
        self.repo.add(Administrator(first_name='Admin', last_name='istrator', user_id=user.id))

    def generate_customers(self, num):
        for i in range(num):
            data = trio.run(self.get_data)
            user = self.create_user(data, self.customer_role)
            address = str(data['results'][0]['location']['street']['number']) + " " + \
                      data['results'][0]['location']['street']['name'] + data['results'][0]['location']['state'] + \
                      data['results'][0]['location']['country']
            new_customer = Customer(first_name=data['results'][0]['name']['first'],
                                    last_name=data['results'][0]['name']['last'],
                                    address=address, phone_no=data['results'][0]['phone'],
                                    credit_card_no=self.generate_credit_card_num(), user_id=user.id)
            self.repo.add(new_customer)

    def generate_airline_companies(self, num):
        if num > 150:  # cant be more than 150 airline_companies
            return
        with open(r"db_generator\airline_companies.json") as f:
            airlines = json.load(f)
        for i in range(num):
            data = trio.run(self.get_data)
            user = self.create_user(data, self.airline_role)
            new_airline = Airline_Company(name=airlines[i]["name"],
                                          country_id=random.randint(1, self.number_of_countries_in_db),
                                          user_id=user.id)
            self.repo.add(new_airline)

    def generate_flights_per_company(self, num):
        airlines = self.repo.get_all(Airline_Company)
        for a in airlines:
            for i in range(num):
                airline_company_id = a.id
                origin_country_id = random.randint(1, self.number_of_countries_in_db)
                destination_country_id = random.randint(1, self.number_of_countries_in_db)
                departure_time = self.fake.date_time_between(start_date='now', end_date='+2y')
                landing_time = departure_time + timedelta(hours=random.randint(2, self.max_hours_delta_t))  # min delta t is 2 hours
                remaining_tickets = self.remaining_tickets_per_flight
                self.repo.add(Flight(airline_company_id=airline_company_id, origin_country_id=origin_country_id,
                                     destination_country_id=destination_country_id, departure_time=departure_time,
                                     landing_time=landing_time, remaining_tickets=remaining_tickets))

    def generate_tickets_per_customer(self, num):
        customers = self.repo.get_all(Customer)
        flights = self.repo.get_all(Flight)
        for c in customers:
            shuffled_flights = random.sample(flights, len(flights))
            flights_for_tickets = shuffled_flights[0:num]
            for f in flights_for_tickets:
                self.repo.add(Ticket(flight_id=f.id, customer_id=c.id))
