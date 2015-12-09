from queue import Queue, Empty
from time import time
from threading import RLock

class EmptyBus(Empty):
    """
    Exceptions raised when no object is on the bus. It wraps queue.Empty
    """

class Bus(object):
    """
    Bus main class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self):
        self.__queue = Queue()
        self.__lock = RLock()

    def post(self, obj):
        """
        Post an object to the bus
        """

        obj.__last_bus_transition_timestamp__ = time()
        self.__lock.acquire()

        try:
            self.__queue.put((obj))
        finally:
            self.__lock.release()

    def next(self, blocking=True, timeout=None):
        """
        Return the next object on the bus.
        blocking -- If True (default), next will return only when an object is available.
        timeout -- In case of blocking call, wait for that number of seconds before returning to the called.
            If None, it will wait undefinitely (default)

        In case of non-blocking call or expired timeout, EmptyBus will be thrown
        """

        if blocking and timeout is None:
            return self.__queue.get()
        else:
            try:
                return self.__queue.get(blocking, timeout)
            except Empty:
                raise EmptyBus()

# vim:sw=4:ts=4:et:

