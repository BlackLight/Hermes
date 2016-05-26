import sys
from threading import RLock

import pyinotify

from ...event.file_system_event import FileSystemEvent
from ...socket import Socket

class InotifySocket(Socket):
    """
    INotify socket. Polls for file events - creation, modification, access,
    removal etc. - using Linux INotify API and generates an event on the
    component bus when one of the monitored resources has generated a certain
    event that matches its filters.

    @requires pyinotify <pip install pyinotify>

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, fs_resource, mask=pyinotify.ALL_EVENTS, n_events=None):
        """
        fs_resource -- Path to the resource to monitor

        mask -- Mask of events to filter - default:  pyinotify.ALL_EVENTS

        n_events -- Events to process before exiting - default: None: loop
        forever or until component stop
        """

        super().__init__(instance=self)
        self._fs_resource = fs_resource
        self._mask = mask
        self._n_events = n_events
        self._processed_events = 0

    def run(self):
        wm = pyinotify.WatchManager()
        wm.add_watch(self._fs_resource, self._mask)

        self._notifier = pyinotify.ThreadedNotifier(wm,
            default_proc_fun=FsEventProcessor(socket=self)
        )

        self._notifier.start()

    def on_event(self, event):
        self._processed_events += 1
        self.fire_event(
            FileSystemEvent(path=event.pathname, mask=event.mask)
        )

        if self._n_events and self._processed_events >= self._n_events:
            self.close()

    def close(self):
        self._notifier.stop()

class FsEventProcessor(pyinotify.ProcessEvent):
    def __init__(self, socket):
        self.__socket = socket

    def process_default(self, event):
        self.__socket.on_event(event)

