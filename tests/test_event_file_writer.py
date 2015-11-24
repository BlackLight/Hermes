import os
import unittest

from evesp.event.mock_event import MockEvent
from evesp.actuator.event_file_writer import EventFileWriter

class TestEventFileWriter(unittest.TestCase):
    def setUp(self):
        basedir = os.path.dirname(os.path.realpath(__file__))
        self.events_file = os.path.join(basedir, 'events.bin')
        self.evt = MockEvent(id=1, name='foo')
        self.fw = EventFileWriter(self.events_file)

    def test_event_file_creation(self):
        self.fw.on_event(self.evt)
        self.assertTrue(os.path.isfile(self.events_file))

    def test_event_correctness(self):
        self.fw.on_event(self.evt)
        with open(self.events_file, 'rb') as fp:
            event_file_content = fp.read()
        fp.close()

        event = MockEvent.deserialize(event_file_content)
        self.assertEqual(event.id, 1)
        self.assertEqual(event.name, 'foo')

    def tearDown(self):
        os.unlink(self.events_file)

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

