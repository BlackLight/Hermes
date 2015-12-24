import re

from evesp.socket.inotify_socket import InotifySocket
from evesp.component import Component

class FileSystemEventComponent(Component):
    """
    File System event component class
    It installs a pool of Inotify sockets to monitor Inotify events (open,
    create, remove, write...) events on file system resources.

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, name, fs_resources=[], n_events=None):
        """
        n_events -- Number of events to fire to the engine
        """

        super().__init__(instance=self, name=name, n_events=n_events)

        # fs_resources is a comma-separated list
        self.fs_resources = re.split('\s*,\s*', fs_resources)

    def run(self):
        inotify_sockets = [InotifySocket(fs_resource=res) for res in self.fs_resources]
        for sock in inotify_sockets: sock.connect(self._component_bus)
        processed_events = 0

        while self.n_events is None or processed_events < self.n_events:
            evt = self._component_bus.next()
            self.fire_event(evt)
            processed_events += 1

        for sock in inotify_sockets: sock.close()

