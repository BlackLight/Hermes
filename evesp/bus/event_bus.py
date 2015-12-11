from evesp.bus import Bus
from evesp.event import Event

class EventBus(Bus):
    """
    Event Bus. Only evesp.event.Event instances can be posted here
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self):
        super().__init__()

    def post(self, obj):
        """
        Post an event to the bus
        """

        assert isinstance(obj, Event)
        super().post(obj)

# vim:sw=4:ts=4:et:

