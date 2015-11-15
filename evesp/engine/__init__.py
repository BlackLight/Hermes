from evesp.bus import Bus

class Engine(object):
    """
    Engine base class
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, config):
        """
        Constructor

        config -- evesp.config.Config object
        """

        self.config = config
        self.classes = {}
        self.components = {}

        for comp_name, component in self.config.components.items():
            if not 'module' in component:
                raise AttributeError('No module name specified for the component name %s - '
                    + 'e.g. evesp.component.mock_component' % (comp_name))

            module_name = component['module']
            module = __import__(module_name, ['*'])
            for module_token in module_name.split('.')[1:]:
                module = getattr(module, module_token)
            self.classes[comp_name] = getattr(module, self.__main_class_name_from_module_name(module_name))

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

    def start(self):
        """
        Start the components listed in the configuration and the engine main loop
        """

        self.bus = Bus(engine=self)

        for name, cls in self.classes.items():
            component = cls(name=name, **(self.config.components[name]))
            component.register(self.bus)
            component.start()

            self.components[name] = component

# vim:sw=4:ts=4:et:

