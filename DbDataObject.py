from custom_errors.DbGenDataNotValidError import DbGenDataNotValidError
from DbDataGen import DbDataGen


class DbDataObject:

    def __init__(self, customers: int, airlines: int, flights_per_airline: int, tickets_per_customer: int):
        self.customers = customers
        self.airlines = airlines
        self.flights_per_airline = flights_per_airline
        self.tickets_per_customer = tickets_per_customer
        self.db_gen = DbDataGen()

    def validate_data(self):
        try:
            airlines = int(self.airlines)
            customers = int(self.customers)
            flights_per_company = int(self.flights_per_airline)
            tickets_per_customer = int(self.tickets_per_customer)
            if airlines < 1 or customers < 1 or flights_per_company < 1 or tickets_per_customer < 1 or airlines > 150:
                raise DbGenDataNotValidError
            if (airlines * flights_per_company) < tickets_per_customer:
                raise DbGenDataNotValidError
        except ValueError:
            raise DbGenDataNotValidError

    def generate_data(self, airlines, customers, flights_per_company, tickets_per_customer):
        self.db_gen.generate_countries()  # send back to rabbit after every task
        self.db_gen.generate_user_roles()
        self.db_gen.generate_admin()
        self.db_gen.generate_airline_companies(airlines)
        self.db_gen.generate_customers(customers)
        self.db_gen.generate_flights_per_company(flights_per_company)
        self.db_gen.generate_tickets_per_customer(tickets_per_customer)

    def __str__(self):
        return f'{{"customers": {self.customers}, "airlines": {self.airlines}, ' \
               f'"flights_per_airline": {self.flights_per_airline},' \
               f' "tickets_per_customer": {self.tickets_per_customer}}}'
