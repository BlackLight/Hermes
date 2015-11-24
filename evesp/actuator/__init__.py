class Actuator(object):
    """
    Base class for actuators
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def on_event(self, event):
        """
        Callback invoked by the engine when an event
        is propagated to the actuator.
        To be implemented by derived classes
        """

        raise NotImplementedError()

# vim:sw=4:ts=4:et:

