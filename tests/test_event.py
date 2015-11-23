import unittest

from evesp.event import Event

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.evt = Event(foo='bar')

    def test_event_creation(self):
        self.assertEqual(self.evt.foo, 'bar')

    def test_non_existing_event(self):
        self.assertRaises(AttributeError, getattr, self.evt, 'non_existing')

    def test_event_pickle_serialization(self):
        ser_evt = self.evt.serialize()
        deser_evt = Event.deserialize(ser_evt)
        self.assertEqual(deser_evt.foo, 'bar')
        self.assertRaises(AttributeError, getattr, deser_evt, 'non_existing')

    def test_event_json_serialization(self):
        ser_evt = self.evt.to_json()
        deser_evt = Event.from_json(ser_evt)
        self.assertEqual(deser_evt.foo, 'bar')
        self.assertRaises(AttributeError, getattr, deser_evt, 'non_existing')

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

