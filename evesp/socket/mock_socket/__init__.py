from evesp.event import mock_event
from evesp.socket import Socket

class MockSocket(Socket):
    """
    Mock component class. It posts a mock event on the component bus and returns
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, config={}, n_events=1):
        super().__init__(instance=self, config=config)
        self.__n_events = n_events

    def run(self):
        processed_events = 0
        while processed_events < self.__n_events:
            evt = mock_event.MockEvent(id=1, name='Test event')
            self.fire_event(evt)
            processed_events += 1

