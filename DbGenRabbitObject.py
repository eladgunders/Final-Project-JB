import pika


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
            print(body)

        self.channel.basic_consume(queue=self.data_to_generate_queue,
                                   on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def consume_to_generated_data(self):
        self.channel.queue_declare(queue=self.generated_data_queue)

        def callback(ch, method, properties, body):
            print(body)

        self.channel.basic_consume(queue=self.generated_data_queue,
                                   on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
