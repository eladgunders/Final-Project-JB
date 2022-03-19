import pika
import json
from DbDataObject import DbDataObject


class DbGenRabbitObject:

    def __init__(self):
        self.data_to_generate_queue = 'DataToGenerate'
        self.generated_data_queue = 'GeneratedData'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def publish_data_to_gen(self, data):
        self.channel.queue_declare(queue=self.data_to_generate_queue)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.data_to_generate_queue,
                                   body=data)

    def publish_generated_data(self, data):
        self.channel.queue_declare(queue=self.generated_data_queue)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.generated_data_queue,
                                   body=data)

    def consume_to_data_to_gen(self):
        self.channel.queue_declare(queue=self.data_to_generate_queue)

        def callback(ch, method, properties, body):
            data = json.loads(body)
            airlines = int(data['airlines'])
            customers = int(data['customers'])
            flights_per_airline = int(data['flights_per_airline'])
            tickets_per_customer = int(data['tickets_per_customer'])
            db_data = DbDataObject(airlines=airlines, customers=customers,
                                   flights_per_airline=flights_per_airline,
                                   tickets_per_customer=tickets_per_customer)
            db_data.generate_data()
            return

        self.channel.basic_consume(queue=self.data_to_generate_queue,
                                   on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def consume_to_generated_data(self):
        self.channel.queue_declare(queue=self.generated_data_queue)

        def callback(ch, method, properties, body):
            print(f'{body} was generated successfully!')

        self.channel.basic_consume(queue=self.generated_data_queue,
                                   on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
