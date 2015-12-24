from .. import Event

class FileSystemEvent(Event):
    """
    Class for mapping file system events - e.g. file, directory or block
    devices creation, removal, access and modification.

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, path, mask, **kwargs):
        """
        path -- Path name that triggered the event
        mask -- Event mask
        """

        super().__init__(kwargs)
        self.path = path
        self.mask = mask

# vim:sw=4:ts=4:et:

