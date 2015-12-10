from evesp.socket.mock_socket import MockSocket
from evesp.component import Component

class MockComponent(Component):
    """
    Mock component class.
    It installs a mock socket and returns when the first event is published

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, name):
        super().__init__(instance=self, name=name)

    def run(self):
        sock = MockSocket()
        sock.connect(self._component_bus)

        evt = self._component_bus.next()
        self.fire_event(evt)

