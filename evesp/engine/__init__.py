from evesp.bus import Bus
from evesp.event_processor.default_event_processor import DefaultEventProcessor

class Engine(object):
    """
    Engine base class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, config, processor_class=DefaultEventProcessor, processor_class_args={}):
        """
        Constructor

        config -- evesp.config.Config object
        processor_class -- A class which extends evesp.event_processor.EventProcessor.
            If not specified, the engine will use its default event processor
        processor_class_args -- Arguments for the constructor of processor_class, if any
        """

        self.config = config
        self.components = {}
        self.__classes = {}
        self.__event_processor = processor_class(**(processor_class_args))

        for comp_name, component in self.config.components.items():
            if not 'module' in component:
                raise AttributeError('No module name specified for the component name %s - '
                    + 'e.g. evesp.component.mock_component' % (comp_name))

            module_name = component['module']
            module = __import__(module_name, ['*'])
            for module_token in module_name.split('.')[1:]:
                module = getattr(module, module_token)
            self.__classes[comp_name] = getattr(module, self.__main_class_name_from_module_name(module_name))

            # Now that it's been used, removed the module key from the component configuration
            del self.config.components[comp_name]['module']

    @staticmethod
    def __main_class_name_from_module_name(module_name):
        """
        By convention, component module names have lowercase with underscore names,
        while their main classes have camel case names
        """
        import re
        return re.sub(r'(^|((?!^)_))([a-zA-Z])', lambda m: m.group(3).upper(), module_name.split('.')[-1])

    def start(self, max_events=None):
        """
        Start the components listed in the configuration and the engine main loop

        max_events -- If set, the engine will stop after having processed that number of events
            Otherwise, it will forever loop for events on the bus to process
        """

        self.bus = Bus(engine=self)

        for name, cls in self.__classes.items():
            component = cls(name=name, **(self.config.components[name]))
            self.components[name] = component

            component.register(self.bus)
            component.start()

        n_events = 0
        while max_events is None or n_events < int(max_events):
            evt = self.bus.next_event()
            n_events += 1
            print("HERE")
            self.__event_processor.on_event(evt)

# vim:sw=4:ts=4:et:

