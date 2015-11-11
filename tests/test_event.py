#!/usr/bin/python

import sys
import unittest

from evesp.event import Event

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.evt = Event(1, foo='bar')

    def test_event_creation(self):
        self.assertEqual(self.evt.id(), 1)
        self.assertEqual(self.evt.get('foo'), 'bar')
        self.assertEqual(self.evt.get('not-existing'), None)

    def test_event_pickle_serialization(self):
        ser_evt = self.evt.serialize()
        deser_evt = Event.deserialize(ser_evt)
        self.assertEqual(deser_evt.id(), 1)
        self.assertEqual(deser_evt.get('foo'), 'bar')
        self.assertEqual(deser_evt.get('not-existing'), None)

    def test_event_json_serialization(self):
        ser_evt = self.evt.to_json()
        deser_evt = Event.from_json(ser_evt)
        self.assertEqual(deser_evt.id(), 1)
        self.assertEqual(deser_evt.get('foo'), 'bar')
        self.assertEqual(deser_evt.get('not-existing'), None)

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

