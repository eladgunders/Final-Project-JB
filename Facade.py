from DbRepo import DbRepo
from db_config import local_session
from sqlalchemy import asc, text, desc


class Facade:

    def __init__(self):
        self.repo = DbRepo(local_session)

    def reset_auto_inc(self, table_class):
        self.repo.reset_auto_inc(table_class)

    def get_all(self, table_class):
        return self.repo.get_all(table_class)

    def get_all_limit(self, table_class, limit_num):
        return self.repo.get_all_limit(table_class, limit_num)

    def get_all_order_by(self, table_class, column_name, direction):
        return self.repo.get_all_order_by(table_class, column_name, direction=asc)

    def get_by_column_value(self, table_class, column_value, value):
        return self.repo.get_by_column_value(table_class, column_value, value)

    def get_by_condition(self, table_class, condition):  # condition is a lambda expression
        return self.repo.get_by_condition(table_class, condition)

    def add(self, one_row):
        self.repo.add(one_row)

    def add_all(self, rows_list):
        self.repo.add_all(rows_list)

    def drop_all_tables(self):
        self.repo.drop_all_tables()