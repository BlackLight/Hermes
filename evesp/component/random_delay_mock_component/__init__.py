from evesp.socket.mock_socket import RandomDelayMockSocket
from evesp.component.mock_component import MockComponent

class RandomDelayMockComponent(MockComponent):
    """
    A component which triggers events using a RandomDelayMockSocket
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, name, n_events=1, max_rnd_delay=1):
        """
        max_rnd_delay -- Maximum number of seconds for the calculation of the random delay between two events
        """

        super().__init__(name=name, n_events=n_events)
        self.__max_rnd_delay = float(max_rnd_delay)

    def run(self):
        sock = RandomDelayMockSocket(n_events=self.n_events, max_rnd_delay=self.__max_rnd_delay)
        sock.connect(self._component_bus)
        processed_events = 0

        while processed_events < self.n_events:
            evt = self._component_bus.next()
            self.fire_event(evt)
            processed_events += 1

