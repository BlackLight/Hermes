from evesp.event import Event

class FileEvent(Event):
    """
    Class for mapping file events
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, path, **kwargs):
        super().__init__(kwargs)
        self.path = path
        self.__validate()

    def __validate(self):
        pass

# vim:sw=4:ts=4:et:

