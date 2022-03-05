from custom_errors.DbGenDataNotValidError import DbGenDataNotValidError
from DbDataGen import DbDataGen


class DbDataObject:

    def __init__(self, customers, airlines, flights_per_airline, tickets_per_customer):
        self.customers = customers
        self.airlines = airlines
        self.flights_per_airline = flights_per_airline
        self.tickets_per_customer = tickets_per_customer
        self.db_gen = DbDataGen('https://randomuser.me/api/?nat=us')

    def validate_and_generate_data(self):
        if (self.airlines * self.flights_per_airline) < self.tickets_per_customer:
            raise DbGenDataNotValidError

        else:
            self.db_gen.generate_countries()  # send back to rabbit after every task
            self.db_gen.generate_user_roles()
            self.db_gen.generate_admin()
            self.db_gen.generate_airline_companies(self.airlines)
            self.db_gen.generate_customers(self.customers)
            self.db_gen.generate_flights_per_company(self.flights_per_airline)
            self.db_gen.generate_tickets_per_customer(self.tickets_per_customer)
