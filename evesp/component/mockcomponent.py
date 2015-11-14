from evesp.component import Component
from evesp.event import Event

class MockComponent(Component):
    def __init__(self, name):
        super().__init__(instance=self, name=name)

    def run(self):
        evt = Event(foo='bar')
        self.bus.post(event=evt)

