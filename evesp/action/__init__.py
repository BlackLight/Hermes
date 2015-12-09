import uuid

class Action(object):
    """
    Base class for actions
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, **kwargs):
        vars(self).update(kwargs)

        # A unique ID that identifies the action along its lifecycle
        self.__action_id = uuid.uuid4()

    def link(self, event):
        """
        Create a link between the action and the event processed by the engine
        that triggered the action.
        """

        # The event that triggered the action
        self.event = event

    def on_event(self, event):
        """
        Execute the logic of the action.
        To be implemented by the derived classes.
        """
        raise NotImplementedError()

    def run(self):
        """
        Shortcut for on_event invoked after the action has been linked to an
        event by the engine,
        """
        self.on_event(self.event)

# vim:sw=4:ts=4:et:

