from evesp.event_processor import EventProcessor

class MockEventProcessor(EventProcessor):
    """
    Mock event processor. It simply appends received events to a list
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self):
        super().__init__()
        self.events = []

    def on_event(self, event):
        self.events.append(event)

# vim:sw=4:ts=4:et:

