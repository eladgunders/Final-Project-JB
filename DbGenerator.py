import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, StringProperty
from DbDataObject import DbDataObject
from custom_errors.DbGenDataNotValidError import DbGenDataNotValidError
from RabbitProducerObject import RabbitProducerObject
from RabbitConsumerObject import RabbitConsumerObject
import json
from db_config import local_session
from data_access_objects.DbRepo import DbRepo
from threading import Thread


class DbGenWidget(Widget):
    airline_companies = ObjectProperty(None)
    customers = ObjectProperty(None)
    flights_per_company = ObjectProperty(None)
    tickets_per_customer = ObjectProperty(None)
    my_progress_bar = ObjectProperty(None)
    alerts_label = StringProperty('')
    repo = DbRepo(local_session)
    rabbit_producer = RabbitProducerObject('DataToGenerate')
    is_db_empty = True

    @staticmethod
    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(data)
        progress_bar_value = list(data.values())[0]
        print(progress_bar_value)

    # root.btn() in kv file
    def btn(self):
        if self.ids.rbutton1.state == 'down':
            if not self.is_db_empty:
                self.ids.alerts_label.text = 'DB already has data. Reset the db to replace the data.'
                return
            try:
                airlines = self.airline_companies.text
                customers = self.customers.text
                flights_per_company = self.flights_per_company.text
                tickets_per_customer = self.tickets_per_customer.text
                db_data_object = DbDataObject(customers=customers, airlines=airlines,
                                              flights_per_airline=flights_per_company,
                                              tickets_per_customer=tickets_per_customer)
                db_data_object.validate_data()
                self.rabbit_producer.publish(json.dumps(db_data_object.__dict__()))
                self.is_db_empty = False

            except DbGenDataNotValidError:
                self.ids.alerts_label.text = 'Data is not Valid!'
        else:
            repo_thread = Thread(target=self.repo.reset_all_tables_auto_inc)
            repo_thread.start()
            self.is_db_empty = True
            self.ids.alerts_label.text = ''

    def switchstate1(self):
        self.ids.rbutton1.state = 'down'
        self.ids.rbutton2.state = 'normal'

    def switchstate2(self):
        self.ids.rbutton2.state = 'down'
        self.ids.rbutton1.state = 'normal'

    def update_progress_bar(self, num):
        self.ids.my_progress_bar.value = num


class MyApp(App):
    def build(self):
        return DbGenWidget()


Builder.load_file('my1.kv')


if __name__ == "__main__":
    rabbit_consumer = RabbitConsumerObject(q_name='GeneratedData', callback=DbGenWidget.callback)
    t1 = Thread(target=rabbit_consumer.consume)
    t1.setDaemon(True)
    t1.start()
    MyApp().run()
