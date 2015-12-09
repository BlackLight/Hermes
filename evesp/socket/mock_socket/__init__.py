from evesp.event import mock_event
from evesp.socket import Socket

class MockSocket(Socket):
    """
    Mock component class. It posts a mock event on the component bus and returns
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, config={}):
        super().__init__(instance=self, config=config)

    def run(self):
        evt = mock_event.MockEvent(id=1, name='Test event')
        self.fire_event(evt)

