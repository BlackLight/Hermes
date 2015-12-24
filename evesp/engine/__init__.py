from enum import Enum
from itertools import cycle
from threading import Thread, Event as ThreadEvent

from evesp.action import ActionResponse, StopAction
from evesp.bus import Bus, EmptyBus
from evesp.bus.event_bus import EventBus
from evesp.component import Component
from evesp.event import Event, StopEvent
from evesp.rules_parser import RulesParser
from evesp.utils import *
from evesp.worker import Worker

class EngineState(Enum):
    Initializing = 'Initializing',
    Ready = 'Ready',
    Running = 'Running',
    StoppingComponents = 'Stopping Components',
    StoppingWorkers = 'Stopping Workers',
    Stopped = 'Stopped'

class Engine(object):
    """
    Engine base class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    # Default number of workers
    __DEFAULT_WORKERS = 5

    # The supervisor by default polls the workers' value bus each 0.01 seconds
    __DEFAULT_WORKER_SUPERVISOR_POLL_PERIOD = 0.01

    # Keep track of actions responses even when the actions are completed (default: False)
    __DEFAULT_TRACK_ACTIONS = False

    def __init__(self, config, atexit_callback=None):
        """
        Constructor

        config -- evesp.config.Config object
        atexit_callback -- Optional method to invoke when the engine has stopped
        """

        self.__state = EngineState.Initializing
        self.config = config

        # Event object use to synchronize the threads when the engine enters "Running" state
        self.__engine_running = ThreadEvent()

        self.components = {}
        self.__atexit_callback = atexit_callback
        self.__classes = {}
        self.__parsed_engine_config = False

        for comp_name, component in self.config.components.items():
            if self.__is_engine_comp_name(comp_name):
                self.__parse_engine_comp_config(component)
            else:
                if not 'module' in component:
                    raise AttributeError('No module name specified for the component name '
                        + comp_name + ' - e.g. evesp.component.mock_component')
                self.__classes[comp_name] = component_class_by_module_name(component['module'])

                # Now that it's been used, removed the module key from the component configuration
                del self.config.components[comp_name]['module']

        if not self.__parsed_engine_config:
            raise AttributeError('The configuration file has no __engine module configuration')

        self.__actions = {}
        self.__create_worker_pool()
        self.__state = EngineState.Ready

    @classmethod
    def __is_engine_comp_name(cls, comp_name):
        return comp_name == '__engine'

    def __engine_parse_n_workers(self, config):
        self.__n_workers = self.__DEFAULT_WORKERS
        if 'workers' in config:
            assert config['workers'].isnumeric()
            self.__n_workers = int(config['workers'])

    def __engine_parse_events_to_process(self, config):
        self.__events_to_process = None
        if 'events_to_process' in config:
            assert config['events_to_process'].isnumeric()
            self.__events_to_process = int(config['events_to_process'])

    def __engine_parse_rules_file(self, config):
        assert 'rules_file' in config
        rules_file = config['rules_file']
        self.__create_event_map(rules_file)

    def __engine_parse_track_actions(self, config):
        self.__track_actions = self.__DEFAULT_TRACK_ACTIONS
        if 'track_actions' in config:
            self.__track_actions = bool(config['track_actions'])

    def __parse_engine_comp_config(self, config):
        self.__parsed_engine_config = True

        self.__engine_parse_n_workers(config)
        self.__engine_parse_events_to_process(config)
        self.__engine_parse_rules_file(config)
        self.__engine_parse_track_actions(config)

    def __create_worker_pool(self):
        workers = [Worker() for worker in range(0, self.__n_workers)]
        self.__workers = workers

        for worker in workers:
            worker.start()

        # Turn the list of workers into a circular pool
        self.__workers_pool = cycle(workers)

        # Workers supervisor thread. It polls the workers' value bus and eventually
        # reacts when values are ready, and stops the workers in case the engine
        # sets the stop flag.
        self.__workers_supervisor = Thread(target = self.__run_workers_supervisor)
        self.__workers_supervisor.start()

    def __run_workers_supervisor(self):
        # Internal object to synchronize on the supervisor exit
        self.__supervisor_exited = ThreadEvent()

        self.__stopped_workers = {}
        workers_pool = cycle(self.__workers_pool)

        for worker in workers_pool:
            try:
                # Thread exit if all the workers have been stopped
                if len(self.__stopped_workers.keys()) == len(self.__workers): break

                action_response = worker._value_bus.next(blocking=True, timeout=self.__DEFAULT_WORKER_SUPERVISOR_POLL_PERIOD)
                if isinstance(action_response, ActionResponse):
                    self.__process_action_response(action_response)
                elif isinstance(action_response, StopEvent):
                    self.__on_worker_stop(worker)
            except EmptyBus: continue

        self.__supervisor_exited.set()

    def __process_action_response(self, action_response):
        action = action_response.get_action()
        action_id = action.get_id()

        if action_id in self.__actions:
            if self.__track_actions:
                self.__actions[action_id] = action_response
            else: del self.__actions[action_id]

    def __on_worker_stop(self, worker):
        self.__stopped_workers[worker.get_id()] = worker

    def __create_event_map(self, rules_file):
        self.__rules_file = rules_file
        self.__rules = RulesParser(self.__rules_file).get_rules()
        self.__rules_by_event_class = {}

        for rule in self.__rules:
            for event in rule['when']:
                event_class = get_full_class_name(event)
                if not event_class in self.__rules_by_event_class:
                    self.__rules_by_event_class[event_class] = []
                self.__rules_by_event_class[event_class].append(rule)

    def __start_components(self):
        for name, cls in self.__classes.items():
            component = cls(name=name, **(self.config.components[name]))
            self.components[name] = component

            component.register(self.__platform_bus)
            component.start()

    def __process_event(self, evt):
        matched_rules = self.__get_matched_rules(evt)

        for rule in matched_rules:
            for action_tmpl in rule['then']:
                action = action_tmpl.link(evt)
                self.__actions[action.get_id()] = action

                worker = self.__next_worker()
                worker._action_bus.post(action)

    def __next_worker(self):
        return next(self.__workers_pool)

    def __get_matched_rules(self, evt):
        evt_class = get_full_class_name(evt)
        if not evt_class in self.__rules_by_event_class:
            # No rules associated to this event type
            return []

        rules_by_class = self.__rules_by_event_class[evt_class]
        matched_rules = []

        # Iterate over the match rules
        for rule in rules_by_class:
            for evt_filter in rule['when']:
                if evt == evt_filter:
                    matched_rules.append(rule)
        return matched_rules

    def start(self):
        """
        Start the components listed in the configuration and the engine main loop
        """

        # Components will publish their events on the platform bus
        self.__platform_bus = EventBus()

        self.__start_components()
        self.__state = EngineState.Running
        self.__engine_running.set()

        n_events = 0
        while self.__events_to_process is None or n_events < self.__events_to_process:
            evt = self.__platform_bus.next()
            n_events += 1
            self.__process_event(evt)

        # Stop the engine after all the events to process have been processed
        self.stop()

    def stop(self):
        """
        Stop the workers, the components, and eventually the engine
        """

        self.__stop_components()
        self.__stop_workers()
        self.__supervisor_exited.wait()
        self.__state = EngineState.Stopped

        if self.__atexit_callback: self.__atexit_callback()

    def is_stopped(self):
        return self.__state == EngineState.Stopped

    def wait_running(self):
        self.__engine_running.wait()

    def __notify_worker_stop(self, worker):
        worker._action_bus.post(StopAction())

    def __stop_workers(self):
        self.__state = EngineState.StoppingWorkers
        for worker in self.__workers:
            self.__notify_worker_stop(worker)

        for worker in self.__workers:
            worker.wait_stop()

    def __stop_components(self):
        self.__state = EngineState.StoppingComponents
        for component_name, component in self.components.items():
            self.__stop_component(component)

    def __stop_component(self, component):
        component._ctrl_bus.post(StopAction())

    def _get_actions(self):
        """
        In case track_actions is False (default), this would return a map
        action_id => Action, containing all the actions currently queued.

        In case track_actions is True (default), this would return a map
        action_id => Action for the actions currently queued, and action_id =>
        ActionResponse for the ones that were completed.
        """

        return self.__actions

# vim:sw=4:ts=4:et:

