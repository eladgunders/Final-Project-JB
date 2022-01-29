from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser
from Logger import Logger
import logging

config = ConfigParser()
config.read("config.conf")
connection_string = config["db"]["conn_string"]

logger = Logger.get_instance()
# if you want to create a table from base the class needs to inherit from declarative_base
Base = declarative_base()

Session = sessionmaker()
engine = create_engine(connection_string, echo=True)  # echo makes the console print all the sql statements being run
local_session = Session(bind=engine)

# creates a table to all classes that inherits from Base
def create_all_entities():
    Base.metadata.create_all(engine)
    logger.logger.debug('Created all sql tables.')