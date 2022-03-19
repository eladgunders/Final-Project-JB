from custom_errors.DbGenDataNotValidError import DbGenDataNotValidError
from DbDataGen import DbDataGen
# from DbGenRabbitObject import DbGenRabbitObject


class DbDataObject:

    def __init__(self, customers: int, airlines: int, flights_per_airline: int, tickets_per_customer: int):
        self.customers = customers
        self.airlines = airlines
        self.flights_per_airline = flights_per_airline
        self.tickets_per_customer = tickets_per_customer
        self.db_gen = DbDataGen()
        # self.rabbit = DbGenRabbitObject()

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

    def generate_data(self):
        self.db_gen.generate_countries()
        #self.rabbit.publish_generated_data('Countries')
        self.db_gen.generate_user_roles()
        #self.rabbit.publish_generated_data('User Roles')
        self.db_gen.generate_admin()
        #self.rabbit.publish_generated_data('Admins')
        self.db_gen.generate_airline_companies(self.airlines)
        #self.rabbit.publish_generated_data('Airlines')
        self.db_gen.generate_customers(self.customers)
        #self.rabbit.publish_generated_data('Customers')
        self.db_gen.generate_flights_per_company(self.flights_per_airline)
        #self.rabbit.publish_generated_data('Flights')
        self.db_gen.generate_tickets_per_customer(self.tickets_per_customer)
        #self.rabbit.publish_generated_data('Tickets')

    def __str__(self):
        return f'{{"customers": {self.customers}, "airlines": {self.airlines}, ' \
               f'"flights_per_airline": {self.flights_per_airline},' \
               f' "tickets_per_customer": {self.tickets_per_customer}}}'

    def __dict__(self):
        return {'customers': self.customers, 'airlines': self.airlines, 'flights_per_airline': self.flights_per_airline,
                'tickets_per_customer': self.tickets_per_customer}
