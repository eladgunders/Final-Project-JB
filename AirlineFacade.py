from FacadeBase import FacadeBase
from Flight import Flight


class AirlineFacade(FacadeBase):

    def __init__(self):
        super().__init__()

    def get_flights_by_airline(self, airline_id):
        if not isinstance(airline_id, int):
            print('Function failed, airline_id must be an integer.')
            return
        if airline_id <= 0:
            print('Function failed, airline_id must be positive.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.airline_company_id == airline_id).all())

    def add_flight(self, flight):
        pass

    def update_airline(self, airline, id_):
        pass

    def update_flight(self, flight, id_):
        pass
