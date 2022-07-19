"""
Run this script when running the main_server.py
"""


from RabbitConsumerObject import RabbitConsumerObject
from ThreadLockManager import ThreadLockManager

import json
from flask import current_app


lock_manager = ThreadLockManager.get_instance()


def main():
    rabbit = RabbitConsumerObject(q_name='db_responses', callback=callback)
    rabbit.consume()


def callback(ch, method, properties, body):
    data = json.loads(body)  # reading the data
    request_id = data['id_']  # getting the request id
    current_app.config['threads_locks_dict'][request_id] = data  # inserting the data with the id to the server dict

    # releasing the right thread and deleting the lock from the lock_manager dict
    lock_manager.locks_dict.pop(request_id).release()
    return


if __name__ == '__main__':
    main()
