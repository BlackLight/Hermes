import enum
import time
import uuid

class ActionState(enum.Enum):
    """
    Enum that maps the states of an action lifecycle
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    create = 'Create'
    link = 'Link'
    start = 'Start'
    end = 'End'
    kill = 'Kill'

class Action(object):
    """
    Base class for actions
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, **kwargs):
        vars(self).update(kwargs)

        # A unique ID that identifies the action along its lifecycle
        self.__action_id = uuid.uuid4()

        # Map of the timestamps for the states of the action
        self.__timestamps = dict(map(lambda state: (state, None), [state for state in ActionState]))
        self.__timestamps[ActionState.create] = time.time()

    def link(self, event):
        """
        Create a link between the action and the event processed by the engine
        that triggered the action.
        """

        # The event that triggered the action
        self.event = event
        self.__timestamps[ActionState.link] = time.time()

    def on_event(self, event):
        """
        Execute the logic of the action.
        To be implemented by the derived classes.

        NOTE: An action should be run only be the engine, and only after having
        it linked to an event. Therefore, if you ever want to manually run an
        action outside of the engine context, you should first link() it to the
        event and then execute run(), so all the states of the action can be
        correctly tracked. on_event should be used directly only in unit tests.
        """

        # Implement this in the derived classes, but always execute the action
        # through run()
        raise NotImplementedError()

    def run(self):
        """
        Shortcut for on_event invoked after the action has been linked to an
        event by the engine,
        """
        self.__timestamps[ActionState.start] = time.time()
        self.on_event(self.event)
        self.__timestamps[ActionState.end] = time.time()

# vim:sw=4:ts=4:et:

