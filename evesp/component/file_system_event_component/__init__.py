import json
import os
import threading

from sqlalchemy import func

from ...db import Db
from ...db.file_system_resource import FileSystemResource
from ...db.file_system_resource_event import FileSystemResourceEvent

from ...socket.inotify_socket import InotifySocket
from .. import Component


class FileSystemEventComponent(Component):
    """
    File System event component class
    It installs a pool of Inotify sockets to monitor Inotify events (open,
    create, remove, write...) events on file system resources.

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, name, fs_resources, n_events=None):
        """
        fs_resources -- File system resources to monitor. It is specified in
        the component section in the configuration file as a JSON string having
        the following format:

        fs_resources: [
            {
                "path": "/path/to/monitor",
                "events": "mask to the pyinotify events to filter (default:ALL)"
            }
        ]

        n_events -- Number of events to fire to the engine
        """

        super().__init__(instance=self, name=name, n_events=n_events)

        self.fs_resources = [
            os.path.abspath(res['path'])
            for res in json.loads(fs_resources)
        ]

        self.db = Db.get_db()
        self.__sync_fs_resources()

    def __sync_fs_resources(self):
        """
        Sync to the database the content of the file system resources
        """

        session = self.db.session()

        try:
            existing_entries = {
                res.path: True
                for res in session.query(FileSystemResource).all()
            }

            missing_entries = list(filter(
                lambda res: res not in existing_entries, self.fs_resources
            ))

            for path in missing_entries:
                if os.path.isdir(path):
                    " TODO "
                elif os.path.isfile(path):
                    with open(path) as f:
                        content = f.read()
                        fs_res = FileSystemResource(path=path, content=content)
                        session.add(fs_res)
            session.commit()
        finally:
            session.close()

    def run(self):
        inotify_sockets = [
            InotifySocket(fs_resource=res)
            for res in self.fs_resources
        ]

        for sock in inotify_sockets:
            sock.connect(self._component_bus)
        processed_events = 0

        while self.n_events is None or processed_events < self.n_events:
            evt = self._component_bus.next()
            threading.Thread(target=self.__store_fs_event, args=(evt,)).start()
            self.fire_event(evt)
            processed_events += 1

        for sock in inotify_sockets:
            sock.close()

    def __store_fs_event(self, event):
        if event.path is None:
            return

        session = self.db.session()

        try:
            res = session.query(FileSystemResource) \
                .filter(FileSystemResource.path == event.path).all()

            if not res:
                return  # This resource is not monitored
            res = res[0]

            if os.path.isfile(res.path):
                last_event = session.query(FileSystemResourceEvent) \
                    .filter(FileSystemResourceEvent.path == res.path) \
                    .filter(
                        FileSystemResourceEvent.created_at ==
                        session.query(
                            func.max(FileSystemResourceEvent.created_at)
                        )
                    ).all()

                if last_event:
                    pass
                    # self.db_session.add(FileSystemResourceEvent(
            else:
                " TODO "
        finally:
            session.close()

    def __get_file_diff(old_content, new_content):
        pass

# vim:sw=4:ts=4:et:
