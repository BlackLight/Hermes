from queue import Queue
from time import time
from threading import RLock

class Bus(object):
    """
    EventBus main class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, engine):
        self.__evt_queue = Queue()
        self.__evt_lock = RLock()

    def post(self, event):
        """
        Post an event to the bus
        """

        event.timestamp = time()
        self.__evt_lock.acquire()

        try:
            self.__evt_queue.put((event))
        finally:
            self.__evt_lock.release()

    def next_event(self):
        """
        Return the next event on the bus
        """
        return self.__evt_queue.get()

# vim:sw=4:ts=4:et:

