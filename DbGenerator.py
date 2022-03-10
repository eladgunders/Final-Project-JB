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
from DbGenRabbitObject import DbGenRabbitObject
import pika
import json
from threading import Thread


class DbGenWidget(Widget):
    airline_companies = ObjectProperty(None)
    customers = ObjectProperty(None)
    flights_per_company = ObjectProperty(None)
    tickets_per_customer = ObjectProperty(None)
    my_progress_bar = ObjectProperty(None)
    alerts_label = StringProperty('')
    rabbit = DbGenRabbitObject()

    # root.btn() in kv file
    def btn(self):
        try:
            airlines = self.airline_companies.text
            customers = self.customers.text
            flights_per_company = self.flights_per_company.text
            tickets_per_customer = self.tickets_per_customer.text
            db_data_object = DbDataObject(customers=customers, airlines=airlines,
                                          flights_per_airline=flights_per_company,
                                          tickets_per_customer=tickets_per_customer)
            db_data_object.validate_data()
            self.rabbit.publish_data_to_gen(db_data_object.__str__())
            self.ids.alerts_label.text = 'The data was generated successfully!'

        except DbGenDataNotValidError:
            self.ids.alerts_label.text = 'Data is not Valid!'

    def switchstate1(self):
        self.ids.rbutton1.state = 'down'
        self.ids.rbutton2.state = 'normal'

    def switchstate2(self):
        self.ids.rbutton2.state = 'down'
        self.ids.rbutton1.state = 'normal'


class MyApp(App):
    def build(self):
        return DbGenWidget()


Builder.load_file('my1.kv')


if __name__ == "__main__":
    MyApp().run()
