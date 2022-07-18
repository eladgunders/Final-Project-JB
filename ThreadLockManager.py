from threading import Lock


class ThreadLockManager:
    _instance = None
    _lock = Lock()

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)

                cls._instance.locks_dict = {}  # request_id[str]: Lock

                return cls._instance
            else:
                return cls._instance

    def lock_thread(self, request_id):
        lock = Lock()  # creating a Lock instance
        self.locks_dict[request_id] = lock  # mapping in with the request id into the dict
        lock.acquire()  # locking with thread
