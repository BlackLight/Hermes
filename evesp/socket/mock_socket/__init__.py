import random
import time

from ...event.mock_event import MockEvent
from .. import Socket


class MockSocket(Socket):
    """
    Mock socket class. It posts n_events mock events (default: 1) on the
    component bus and returns
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, n_events=1):
        super().__init__(instance=self)
        self._n_events = n_events

    def run(self):
        processed_events = 0
        while processed_events < self._n_events:
            evt = MockEvent(id=1, name='Test event')
            self.fire_event(evt)
            processed_events += 1


class RandomDelayMockSocket(MockSocket):
    """
    A mock socket class which posts n_events at random intervals to the
    component bus
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, n_events=1, max_rnd_delay=1):
        """
        max_rnd_delay -- Maximum number of seconds for the calculation of
        the random delay between two events
        """
        super().__init__(n_events=n_events)
        self.__max_rnd_delay = max_rnd_delay

    def run(self):
        processed_events = 0
        while processed_events < self._n_events:
            time.sleep(random.uniform(0, self.__max_rnd_delay))
            evt = MockEvent(id=1, name='Test event')
            self.fire_event(evt)
            processed_events += 1
