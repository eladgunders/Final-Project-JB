from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# user-name: postgres
# password: admin
# database: sqlalchemy_test
connection_string = 'postgresql+psycopg2://postgres:admin@localhost/flights_db_tests'

# if you want to create a table from base the class needs to inherit from declarative_base
Base = declarative_base()

Session = sessionmaker()
engine = create_engine(connection_string, echo=True)  # echo makes the console print all the sql statements being run
local_session = Session(bind=engine)

# creates a table to all classes that inherits from Base
def create_all_entities():
    Base.metadata.create_all(engine)