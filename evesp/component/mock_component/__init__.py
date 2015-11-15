from evesp.event import mock_event
from evesp.component import Component

class MockComponent(Component):
    """
    Mock component class. It posts a mock event on the bus and returns
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, name):
        super().__init__(instance=self, name=name)

    def run(self):
        evt = mock_event.MockEvent(id=1, name='Test event')
        self.bus.post(event=evt)

