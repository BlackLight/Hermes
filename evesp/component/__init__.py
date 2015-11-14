from threading import Thread

from evesp.bus import Bus

class Component(object):
    """
    Base class for components
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, instance, name):
        """
        Static method to initialize the common property for a component

        instance  -- Instance of Component to be started
        name -- Component unique name
        """
        self.name = name
        self.instance = instance

    def register(self, bus):
        """
        Register the component to the bus

        bus -- evesp.bus object where the component will publish it events
        """
        self.instance.bus = bus

    def start(self):
        """
        Start the component as a separated thread.
        Derived classes must implement the run() method
        """
        self.__thread = Thread(target = self.instance.run)
        self.__thread.start()

    def stop(self):
        # TBD
        raise NotImplementedError()

# vim:sw=4:ts=4:et:

