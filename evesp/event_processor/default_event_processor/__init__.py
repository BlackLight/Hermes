from evesp.event_processor import EventProcessor

class DefaultEventProcessor(EventProcessor):
    """
    Default event processor for the engine
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self):
        super().__init__()

    def on_event(self, event):
        # TBD
        ...

# vim:sw=4:ts=4:et:

