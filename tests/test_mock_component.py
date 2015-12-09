import os
import pickle
import sys
import time
import unittest

from evesp.config import Config
from evesp.engine import Engine
from evesp.event.mock_event import MockEvent
from evesp.component.mock_component import MockComponent

class TestMockComponent(unittest.TestCase):
    comp_name = 'My Mock Component'
    event_bin_file = os.path.join('tests', 'events.bin')

    def setUp(self):
        try:
            os.unlink(self.event_bin_file)
        except FileNotFoundError:
            pass

        basedir = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(basedir, 'conf', 'test_mock_component.conf')
        self.engine = Engine( config = Config(config_file) )
        self.engine.start()

    def test_mock_component(self):
        self.assertTrue(self.comp_name in self.engine.components)
        component = self.engine.components[self.comp_name]
        self.assertTrue(isinstance(component, MockComponent))

        poll_secs = 0.01
        waited_secs = 0
        timeout = 5

        while waited_secs < timeout:
            if not os.path.isfile(self.event_bin_file):
                time.sleep(poll_secs)
                waited_secs += poll_secs
            else:
                break

        self.assertTrue(os.path.isfile(self.event_bin_file))

        with open(self.event_bin_file, 'rb') as fp:
            events = []

            while True:
                try:
                    events.append(pickle.load(fp))
                except EOFError:
                    break

        self.assertTrue(len(events) == 1)
        evt = events[0]
        self.assertTrue(isinstance(evt, MockEvent))
        self.assertEqual(evt.id, 1)
        self.assertEqual(evt.name, 'Test event')

    def tearDown(self):
        try:
            os.unlink(self.event_bin_file)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

