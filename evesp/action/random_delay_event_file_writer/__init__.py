import random
import time

from evesp.action.event_file_writer import EventFileWriter

class RandomDelayEventFileWriter(EventFileWriter):
    """
    An event file writer which triggers events with random delays - for testing
    purposes

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, filepath, max_rnd_delay=1):
        """
        max_rnd_delay -- Maximum delay, in seconds, the worker will wait before
        posting the action
        """

        super().__init__(filepath=filepath)
        self.__max_rnd_delay = float(max_rnd_delay)

    def on_event(self, event):
        super().on_event(event)
        time.sleep(random.uniform(0, self.__max_rnd_delay))

# vim:sw=4:ts=4:et:

