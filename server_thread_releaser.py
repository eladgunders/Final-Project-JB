"""
Run this script when running the main_server.py
"""


from RabbitConsumerObject import RabbitConsumerObject
from ThreadLockManager import ThreadLockManager

import json


lock_manager = ThreadLockManager.get_instance()


def main():
    rabbit = RabbitConsumerObject(q_name='db_responses', callback=callback)
    rabbit.consume()


def callback(ch, method, properties, body):
    data = json.loads(body)  # reading the data
    request_id = data['id_']  # getting the request id
    lock_manager.handle_answer_release_thread(request_id=request_id, data=data)
    return


if __name__ == '__main__':
    main()
