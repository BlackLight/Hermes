import unittest

from evesp.event import Event, AttributeValueAny
from evesp.event.mock_event import MockEvent


class MyEvent(Event):
    def __init__(self, id, name):
        super().__init__(id=id, name=name)


class TestEventCompare(unittest.TestCase):
    def setUp(self):
        self.evt = MockEvent(id=1, name='foo')

    def test_event_equals(self):
        mock_event = MockEvent(id=1, name='foo')
        self.assertTrue(mock_event == self.evt)

    def test_event_equals_ignore(self):
        mock_event = MockEvent(id=1, name=AttributeValueAny())
        self.assertTrue(mock_event == self.evt)

        mock_event = MockEvent(id=AttributeValueAny(), name='foo')
        self.assertTrue(mock_event == self.evt)

        mock_event = MockEvent(id=AttributeValueAny(), name=AttributeValueAny())
        self.assertTrue(mock_event == self.evt)

    def test_event_not_equals_value(self):
        mock_event = MockEvent(id=2, name='foo')
        self.assertFalse(mock_event == self.evt)

    def test_event_not_equals_type(self):
        mock_event = MyEvent(id=1, name='foo')
        self.assertFalse(mock_event == self.evt)

    def test_event_not_equals_type_attr(self):
        mock_event = MyEvent(id=2, name='foo')
        self.assertFalse(mock_event == self.evt)

    def test_event_equals_parent_type(self):
        mock_event = Event(id=1, name='foo')
        self.assertTrue(mock_event == self.evt)

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:
