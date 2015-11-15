from evesp.event_processor import EventProcessor

class MockEventProcessor(EventProcessor):
    """
    Mock event processor. It take a custom event handler as parameter
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, event_hndl):
        super().__init__()
        self.__event_hndl = event_hndl

    def on_event(self, event):
        self.__event_hndl(event)

# vim:sw=4:ts=4:et:

