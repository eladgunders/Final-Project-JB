from sqlalchemy import asc, text, desc


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def reset_auto_inc(self, table_class):
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY')

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


