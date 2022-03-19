from DbGenRabbitObject import DbGenRabbitObject


def main():
    rabbit = DbGenRabbitObject()
    rabbit.consume_to_data_to_gen()


if __name__ == '__main__':
    main()
