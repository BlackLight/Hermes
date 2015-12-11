from itertools import cycle
from threading import Thread

from evesp.action import StopAction
from evesp.bus import Bus, EmptyBus
from evesp.bus.event_bus import EventBus
from evesp.component import Component
from evesp.event import Event, StopEvent
from evesp.rules_parser import RulesParser
from evesp.utils import *
from evesp.worker import Worker, WorkerState

class Engine(object):
    """
    Engine base class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    # Default number of workers
    __DEFAULT_WORKERS = 5

    # The supervisor by default polls the workers' value bus each 0.01 seconds
    __DEFAULT_WORKER_SUPERVISOR_POLL_PERIOD = 0.01

    def __init__(self, config):
        """
        Constructor

        config -- evesp.config.Config object
        """

        self.__stopped = False
        self.config = config
        self.components = {}
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

        self.__create_worker_pool()

    @classmethod
    def __is_engine_comp_name(cls, comp_name):
        return comp_name == '__engine'

    def __parse_engine_comp_config(self, component):
        self.__parsed_engine_config = True

        ##
        # n_workers
        ##
        self.__n_workers = self.__DEFAULT_WORKERS
        if 'workers' in component:
            assert component['workers'].isnumeric()
            self.__n_workers = int(component['workers'])

        ##
        # events_to_process
        ##
        self.__events_to_process = None
        if 'events_to_process' in component:
            assert component['events_to_process'].isnumeric()
            self.__events_to_process = int(component['events_to_process'])

        ##
        # rules_file
        ##
        assert 'rules_file' in component
        rules_file = component['rules_file']

        self.__create_event_map(rules_file)

    def __create_worker_pool(self):
        workers = [Worker() for worker in range(0, self.__n_workers)]
        self.__workers = workers

        for worker in workers:
            worker.start()

        # Turn the list of workers into a circular pool
        self.__workers_pool = cycle(workers)

        # Workers supervisor thread. It polls the workers' value bus and eventually
        # reacts when values are ready, and stops the workers in case the engine
        # sets the shutdown flag.
        self.__workers_supervisor = Thread(target = self.__run_workers_supervisor)
        self.__workers_supervisor.start()

    def __run_workers_supervisor(self):
        worker_idx = 0
        while self.__workers:
            worker = self.__workers[worker_idx]
            if worker.get_state() == WorkerState.stopped:
                # Remove the stopped worker from the list and update the pool
                del self.__workers[worker_idx]
                self.__workers_pool = cycle(self.__workers)

            # Poll the value bus
            try:
                ret_value = worker._value_bus.next(blocking=True, timeout=self.__DEFAULT_WORKER_SUPERVISOR_POLL_PERIOD)

                ##
                # TODO Do something with the value
                ##

            except EmptyBus:
                pass

            if self.__workers:
                worker_idx %= (len(self.__workers))

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
            for action in rule['then']:
                action.link(evt)
                worker = self.__next_worker()
                worker._action_bus.post(action)

    def __next_worker(self):
        # XXX This is a circular list. Need to come out with a better
        # scheduling algorithm for the workers based on how much work
        # is stuck in their queue
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

        n_events = 0
        while self.__events_to_process is None or n_events < self.__events_to_process:
            evt = self.__platform_bus.next()
            n_events += 1
            self.__process_event(evt)

        # Shutdown the engine after all the events to process have been processed
        self.stop()

    def stop(self):
        """
        Shutdown the workers, the components, and eventually the engine
        """

        self.__stopped = True
        self.__shutdown_workers()
        self.__shutdown_components()

    def is_stopped(self):
        return self.__stopped

    def __shutdown_workers(self):
        for worker in self.__workers:
            worker._action_bus.post(StopAction())

    def __shutdown_components(self):
        for component_name, component in self.components.items():
            self.__shutdown_component(component)

    def __shutdown_component(self, component):
        # TODO Add log traces when sending stop events to components
        component._ctrl_bus.post(StopAction())

# vim:sw=4:ts=4:et:

