from evesp.bus import Bus
from evesp.action import Action

class ActionBus(Bus):
    """
    Action Bus. Only evesp.event.Action instances can be posted here
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self):
        super().__init__()

    def post(self, obj):
        """
        Post an action to the bus
        """

        assert isinstance(obj, Action)
        super().post(obj)

# vim:sw=4:ts=4:et:

