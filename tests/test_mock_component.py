import os
import pickle
import threading
import unittest

from evesp.config import Config
from evesp.engine import Engine
from evesp.event.mock_event import MockEvent
from evesp.component.mock_component import MockComponent


class TestMockComponent(unittest.TestCase):
    comp_name = 'my_mock_component'
    event_bin_file = os.path.join('tests', 'events.bin')

    def setUp(self):
        # Clean up the event file
        try:
            os.unlink(self.event_bin_file)
        except FileNotFoundError:
            pass

        # Synchronize on this event to wait the engine stop
        self.engine_stopped = threading.Event()

        config = Config(
            __engine__={
                # rules can either be a JSON file or a Python object
                # 'rules': 'tests/rules/test_mock_component_rules.json',
                'rules': [
                    {
                        # Display name for the rule
                        'label': 'Test rule 1',
                        'when': [
                            {
                                # React when receiving a MockEvent with id=1
                                'class': 'MockEvent',
                                'attributes': {
                                    'id': 1
                                }
                            }
                        ],

                        'then': [
                            # Trigger an EventFileWriter action that will write
                            # the received event to the filepath argument
                            {
                                'class': 'EventFileWriter',
                                'arguments': {
                                    'filepath': 'tests/events.bin'
                                }
                            }
                        ]
                    }
                ],
                'db_path': 'tests/main.db',

                # Stop the engine after receiving the first event
                # (default: listen for event indefinitely)
                'events_to_process': '1',

                # Spawn 3 workers for running the action
                'workers': '3',
            },

            my_mock_component={
                # Module name for the component to be spawned
                'module': 'evesp.component.mock_component',
            }
        )

        self.engine = Engine(
            config=config,
            # Callback to be invoked when the engine has terminated
            on_exit=self.__on_engine_exit)

        self.engine.start()

    def __on_engine_exit(self):
        self.engine_stopped.set()

    def test_mock_component(self):
        # Wait for the engine to stop
        self.engine_stopped.wait()

        self.assertTrue(self.comp_name in self.engine.components)
        component = self.engine.components[self.comp_name]
        self.assertTrue(isinstance(component, MockComponent))
        self.assertTrue(os.path.isfile(self.event_bin_file))

        with open(self.event_bin_file, 'rb') as fp:
            events = []
            while True:
                try:
                    evt = pickle.load(fp)
                    events.append(evt)
                except EOFError:
                    break

        self.assertEqual(len(events), 1)
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
