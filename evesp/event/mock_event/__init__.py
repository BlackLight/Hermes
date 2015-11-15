from evesp.event import Event

class MockEvent(Event):
    """
    Mock event class, just having id and name as attributes
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, id, name):
        super().__init__(id=id, name=name)

# vim:sw=4:ts=4:et:

