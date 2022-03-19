from db_config import local_session, create_all_entities
from data_access_objects.DbRepo import DbRepo


# creating the db
repo = DbRepo(local_session)
create_all_entities()  # create tables if not exist
repo.create_all_sp('sp_flights_db.sql')
repo.reset_all_tables_auto_inc()

