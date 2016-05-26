import os
import pickle
import threading
import time
import unittest

from evesp.config import Config
from evesp.engine import Engine
from evesp.event.file_system_event import FileSystemEvent
from evesp.component.file_system_event_component import FileSystemEventComponent


class TestFileSystemEventComponent(unittest.TestCase):
    comp_name = 'File system event component'
    event_bin_file = os.path.join('tests', 'events.bin')
    watched_file = os.path.join('tests', 'mock_file')
    db_file = os.path.join('tests', 'main.db')

    def __create_mock_file(self):
        with open(self.watched_file, 'w') as fp:
            fp.write('original content')

    def __cleanup(self):
        for f in [self.event_bin_file, self.watched_file, self.db_file]:
            try:
                os.unlink(f)
            except FileNotFoundError:
                pass

    def setUp(self):
        self.__cleanup()
        self.__create_mock_file()

        # Synchronize on this event to wait the engine stop
        self.engine_stopped = threading.Event()

        basedir = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(
            basedir, 'conf', 'test_file_system_event_component.conf'
        )

        self.engine = Engine(
            config=Config(config_file),
            atexit_callback=self.__on_engine_exit
        )

        threading.Thread(target=self.engine.start).start()

        self.engine.wait_running()
        time.sleep(0.1)
        threading.Thread(target=self.__create_mock_file).start()

    def __on_engine_exit(self):
        self.engine_stopped.set()

    def test_file_system_event_component(self):
        self.engine_stopped.wait()

        self.assertTrue(self.comp_name in self.engine.components)
        component = self.engine.components[self.comp_name]
        self.assertTrue(isinstance(component, FileSystemEventComponent))
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
        self.assertTrue(isinstance(evt, FileSystemEvent))

    def tearDown(self):
        self.__cleanup()

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:
