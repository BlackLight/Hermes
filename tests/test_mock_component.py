import os
import sys
import unittest

from evesp.config import Config
from evesp.engine import Engine
from evesp.event.mock_event import MockEvent
from evesp.component.mock_component import MockComponent
from evesp.event_processor.mock_event_processor import MockEventProcessor

class TestEngine(unittest.TestCase):
    comp_name = 'My Mock Component'
    events = []

    def event_hndl(self, event):
        self.events.append(event)

    def setUp(self):
        basedir = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(basedir, 'conf', 'test_mock_component.conf')
        self.engine = Engine(
            config = Config(config_file),
            processor_class = MockEventProcessor,
            processor_class_args = { 'event_hndl': self.event_hndl }
        )

        self.engine.start(max_events=1)

    def test_mock_component(self):
        self.assertTrue(self.comp_name in self.engine.components)
        component = self.engine.components[self.comp_name]
        self.assertTrue(isinstance(component, MockComponent))

        self.assertTrue(len(self.events) == 1)
        evt = self.events[0]
        self.assertTrue(isinstance(evt, MockEvent))
        self.assertEqual(evt.id, 1)
        self.assertEqual(evt.name, 'Test event')

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

