import os
import unittest

from evesp.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        basedir = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(basedir, 'conf', 'test_config.conf')
        self.config = Config(config_file)

    def test_attributes(self):
        self.assertEqual(self.config.section_1.value_1, '42')
        self.assertEqual(self.config.section_1.value_2, 'feedbeef')
        self.assertEqual(self.config.section_1.foobar, 'Lorem Ipsum')
        self.assertRaises(AttributeError, getattr, self.config, 'section_1.non_existing')
        self.assertEqual(self.config.section_2.value_unicode, 'ùnìçødè')
        self.assertRaises(AttributeError, getattr, self.config, 'section_2.non_existing')
        self.assertRaises(AttributeError, getattr, self.config, 'section_non_existing.value_1')
        self.assertRaises(AttributeError, getattr, self.config, 'section_non_existing.non_existing')

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

