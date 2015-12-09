import uuid

class Action(object):
    """
    Base class for actions
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def sign(self, event):
        """
        An action is signed when the engine pushes it to a worker to be processed.
        The signing process implies that a unique ID is generated for the action,
        used to track it along its lifecycle, and the event that triggered the
        action will be attached to the object.
        """

        self.action_id = uuid.uuid4()

        # The original event that triggered the action
        self.event = event

    def on_event(self, event):
        """
        Execute the logic of the action.
        To be implemented by the derived classes.
        """
        raise NotImplementedError()

    def run(self):
        """
        Shortcut for on_event invoked after the action has been signed,
        therefore an event has already been attached to it.
        """
        self.on_event(self.event)

# vim:sw=4:ts=4:et:

