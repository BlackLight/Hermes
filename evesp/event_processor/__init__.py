class EventProcessor(object):
    """
    Event processor base class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def on_event(self, event):
        raise NotImplementedError()

# vim:sw=4:ts=4:et:

