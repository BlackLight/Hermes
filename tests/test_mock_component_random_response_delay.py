import os
import pickle
import sys
import threading
import time
import unittest

from evesp.action import ActionResponse, SuccessActionResponse
from evesp.component.random_delay_mock_component import RandomDelayMockComponent
from evesp.config import Config
from evesp.engine import Engine
from evesp.event.mock_event import MockEvent

class TestMockComponent(unittest.TestCase):
    comp_name = 'My Mock Component'
    event_bin_file = os.path.join('tests', 'events.bin')
    n_events = 10

    def setUp(self):
        try: os.unlink(self.event_bin_file)
        except FileNotFoundError: pass

        # Synchronize on this event to wait the engine stop
        self.engine_stopped = threading.Event()

        basedir = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(basedir, 'conf', 'test_mock_component_random_response_delay.conf')
        self.engine = Engine( config = Config(config_file), on_exit = self.__on_engine_exit )
        self.engine.start()

    def __on_engine_exit(self):
        self.engine_stopped.set()

    def test_mock_component(self):
        self.engine_stopped.wait()

        self.assertTrue(self.comp_name in self.engine.components)
        component = self.engine.components[self.comp_name]
        self.assertTrue(isinstance(component, RandomDelayMockComponent))
        self.assertTrue(os.path.isfile(self.event_bin_file))

        with open(self.event_bin_file, 'rb') as fp:
            events = []
            while True:
                try:
                    evt = pickle.load(fp)
                    events.append(evt)
                except EOFError: break

        self.assertEqual(len(events), self.n_events)
        for evt in events:
            self.assertTrue(isinstance(evt, MockEvent))
            self.assertEqual(evt.id, 1)
            self.assertEqual(evt.name, 'Test event')

        actions = self.engine._get_actions()
        self.assertTrue(len(actions) == self.n_events)

        for action_response in actions.values():
            self.assertTrue(isinstance(action_response, SuccessActionResponse))

    def tearDown(self):
        try: os.unlink(self.event_bin_file)
        except FileNotFoundError: pass

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

