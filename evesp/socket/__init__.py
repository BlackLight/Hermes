from threading import Thread

class Socket(object):
    """
    Base class for sockets
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, instance):
        """
        Initialize the common property for a socket

        instance  -- Instance of Socket to be started - used to invoke the run method
        """

        if isinstance(instance, self.__class__) is False:
            raise AttributeError('Got [%s] instance, expected an instance of [%s]' % (type(instance), type(self)))

        self.instance = instance

    def connect(self, bus):
        """
        Connect the socket to the specified component bus
        and execute the run() method on a separated thread.
        Derived classes must implement the run() method.

        bus -- Component bus where the events will be pushed
        """

        self.instance.__bus = bus
        self.__thread = Thread(target = self.instance.run)
        self.__thread.start()

    def close(self):
        """
        Clean socket cleanup. To be implemented by derived classes.
        """
        pass

    def fire_event(self, event):
        """
        Send an event to the component bus
        """

        self.__bus.post(event)

# vim:sw=4:ts=4:et:

