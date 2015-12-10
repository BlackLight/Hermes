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

        self.__stopped = False
        self.name = name
        self.instance = instance
        self.config = config

        # Direction: component [internal]
        #
        # Your component can manage this bus internally for any purposes - e.g.
        # sockets and internal events
        self._component_bus = Bus()

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
        if isinstance(evt, StopEvent):
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

        # ####
        # TODO Manage shutdown conciliation with the engine, queues of pending
        # events to push to the __platform_bus before the shutdown is completed,
        # and eventually thread signals and kills in case the component is
        # hanging
        # ####

    def fire_event(self, event):
        """
        Standard API for firing events
        Set the component field on the event before posting it to the bus
        """

        # A component cannot fire a stop event to the engine
        assert not isinstance(event, StopEvent)

        event.component = self.name
        self.__platform_bus.post(event)

# vim:sw=4:ts=4:et:

