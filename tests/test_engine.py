import os
import sys
import unittest

from evesp.config import Config
from evesp.engine import Engine

class TestEngine(unittest.TestCase):
    def setUp(self):
        basedir = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(basedir, 'conf', 'test_engine.conf')
        self.engine = Engine(Config(config_file))

    def test_component_registration(self):
        self.engine.start()
        # print(self.engine.config.components)
        # self.assertEqual(self.evt.get('foo'), 'bar')
        # self.assertEqual(self.evt.get('not-existing'), None)

    # def test_event_pickle_serialization(self):
    #     ser_evt = self.evt.serialize()
    #     deser_evt = Event.deserialize(ser_evt)
    #     self.assertEqual(deser_evt.get('foo'), 'bar')
    #     self.assertEqual(deser_evt.get('not-existing'), None)

    # def test_event_json_serialization(self):
    #     ser_evt = self.evt.to_json()
    #     deser_evt = Event.from_json(ser_evt)
    #     self.assertEqual(deser_evt.get('foo'), 'bar')
    #     self.assertEqual(deser_evt.get('not-existing'), None)

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

