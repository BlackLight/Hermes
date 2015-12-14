from evesp.socket.mock_socket import MockSocket, RandomDelayMockSocket
from evesp.component import Component

class MockComponent(Component):
    """
    Mock component class.
    It installs a mock socket and returns when the first event is published

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, name, n_events=1):
        """
        n_events -- Number of events to fire to the engine
        """

        super().__init__(instance=self, name=name)
        self._n_events = int(n_events)

    def run(self):
        sock = MockSocket(n_events=self._n_events)

        sock.connect(self._component_bus)
        processed_events = 0

        while processed_events < self._n_events:
            evt = self._component_bus.next()
            self.fire_event(evt)
            processed_events += 1

