from enum import Enum
from threading import Thread, RLock
from time import sleep
from uuid import uuid4

from evesp.action import *
from evesp.bus import Bus
from evesp.bus.action_bus import ActionBus
from evesp.event import StopEvent
from evesp.utils import *

class WorkerState(Enum):
    Initializing = 'Initializing'
    Ready = 'Ready'
    Idle  = 'Idle'
    Running = 'Running'
    Stopping = 'Stopping'
    Stopped = 'Stopped'

class Worker(object):
    """
    Worker base class.

    A worker is a thread spawned by an engine which can run the logic of an
    actuator.

    An engine usually spawns a pool of workers, an they communicate to each
    other over two queues.

    _action_bus - A queue of actions passed by the engine to the worker.

    _value_bus - A queue of returned values, passed by the worker back to the
    engine when the code of the actuator has been executed.

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self):
        """
        Constructor. It will build:

        _action_bus -- Bus object connected to the engine. The actions will be
        passed by the engine over here.

        _value_bus -- Bus object connected to the engine. The values of the
        actions run by the worker will be passed.
        """

        self.__state_lock = RLock()
        self.__set_state(WorkerState.Initializing)
        self.__id = str(uuid4())

        self._action_bus = ActionBus()
        self._value_bus = Bus()
        self.__processed_actions = 0

        self.__set_state(WorkerState.Ready)

    def start(self, actions_to_run=None):
        """
        Start the worker, which then polls _action_bus for actions to run.

        actions_to_run -- If set, the worker will stop after having processed that
        number of actions.  Otherwise, it will forever loop for actions on the
        bus to process.
        """

        self.__thread = Thread(target = self.__run, args=[actions_to_run])
        self.__thread.start()
        self.__set_state(WorkerState.Idle)

    def __run(self, actions_to_run):
        while actions_to_run is None or self.__processed_actions < actions_to_run:
            action = self._action_bus.next()
            if isinstance(action, StopAction):
                self.stop()
                break   # Worker thread exit

            self.__process_action_response(
                self.__execute_action(action)
            )

    def __execute_action(self, action):
        self.__set_state(WorkerState.Running)
        try:
            action_return = action.run()
            return SuccessActionResponse(action=action, response=action_return)
        except Exception as e:
            action_return = e
            return ErrorActionResponse(action=action, response=action_return)

    def __notify_stop(self):
        self._value_bus.post(StopEvent())

    def __process_action_response(self, response):
        self.__processed_actions += 1
        try:
            self._value_bus.post(response)
        finally:
            self.__set_state(WorkerState.Idle)

    def __set_state(self, state):
        assert isinstance(state, WorkerState)
        self.__state_lock.acquire()

        try: self.__state = state
        finally: self.__state_lock.release()

    def stop(self):
        """
        Worker stop
        """
        self.__set_state(WorkerState.Stopping)
        self.__notify_stop()
        self.__set_state(WorkerState.Stopped)

    def is_stopped(self):
        return self.get_state() == WorkerState.Stopped

    def wait_stop(self):
        """
        Wait for the internal thread to terminate
        """

        if not self.is_stopped():
            self.__thread.join()

    def get_state(self):
        return self.__state

    def get_id(self):
        return self.__id

# vim:sw=4:ts=4:et:

