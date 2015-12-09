from threading import Thread

from evesp.bus import Bus
from evesp.event import StopEvent

class Component(object):
    """
    Base class for components
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, instance, name, config = {}):
        """
        Initialize the common property for a component

        instance  -- Instance of Component to be started - used to invoke the run method
        name -- Component unique name
        config -- Component configuration as a dictionary
        """

        if isinstance(instance, self.__class__) is False:
            raise AttributeError('Got [%s] instance, expected an instance of [%s]' % (type(instance), type(self)))

        self.name = name
        self.instance = instance
        self.config = config
        self.component_bus = Bus()

    def register(self, bus):
        """
        Register the component to the bus

        bus -- evesp.bus object where the component will publish it events
        """

        self.instance.engine_bus = bus

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

    def fire_event(self, event):
        """
        Standard API for firing events
        Set the component field on the event before posting it to the bus
        """

        # A component cannot fire a stop event to the engine
        assert not isinstance(event, StopEvent)

        event.component = self.name
        self.engine_bus.post(event)

# vim:sw=4:ts=4:et:

