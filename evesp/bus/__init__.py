from pydispatch import dispatcher

from evesp import event

class Bus(object):
    """
    EventBus main class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self):
        dispatcher.connect(self.__event_handler, signal=dispatcher.Any, sender=dispatcher.Any)

    def __event_handler(self, event):
        print(event)

    def post(self, event):
        dispatcher.send(signal=dispatcher.Any, event=event)

# vim:sw=4:ts=4:et:

