from threading import Thread

from evesp.action import StopAction
from evesp.bus import Bus
from evesp.bus.event_bus import EventBus, Bus
from evesp.event import Event

class Component(object):
    """
    Base class for components
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, instance, name, n_events=None, config = {}):
        """
        Initialize the common property for a component

        instance  -- Instance of Component to be started - used to invoke the run method
        name -- Component unique name
        n_events -- Number of events to fire to the engine before exiting (default: None, loop forever)
        config -- Component configuration as a dictionary
        """

        if isinstance(instance, self.__class__) is False:
            raise AttributeError('Got [%s] instance, expected an instance of [%s]' % (type(instance), type(self)))

        self.__stopped = False
        self.name = name
        self.instance = instance
        self.n_events = int(n_events) if n_events else None
        self.config = config

        # Direction: component [internal]
        #
        # Your component can manage this bus internally for any purposes - e.g.
        # sockets and internal events
        self._component_bus = EventBus()

        # Direction: engine -> component
        #
        # The component will listen here for internal messages from the engine
        # (like stop events) and process them
        self._ctrl_bus = Bus()

    def register(self, platform_bus):
        """
        Register the component to the bus

        __platform_bus -- Direction: component -> engine. Bus object connected to
        the engine where the component will publish its events.
        """

        self.instance.__platform_bus = platform_bus

        # Start a thread that loops on the component bus for messages from the engine
        self.__ctrl_bus_loop_thread = Thread(target = self.instance.__ctrl_bus_loop)
        self.__ctrl_bus_loop_thread.start()

    def __ctrl_bus_loop(self):
        while self.__stopped is False:
            evt = self._ctrl_bus.next()
            self.__process_engine_event(evt)

    def __process_engine_event(self, evt):
        if isinstance(evt, StopAction):
            self.stop()

    def start(self):
        """
        Start the component as a separated thread.
        Derived classes must implement the run() method
        """

        self.__thread = Thread(target = self.instance.run)
        self.__thread.start()

    def stop(self):
        """
        Clean shutdown method
        """
        self.__stopped = True

    def is_stopped(self):
        return self.__stopped

    def fire_event(self, event):
        """
        Standard API for firing events
        Set the component field on the event before posting it to the bus
        """

        assert isinstance(event, Event)
        event._component = self.name
        self.__platform_bus.post(event)

# vim:sw=4:ts=4:et:

