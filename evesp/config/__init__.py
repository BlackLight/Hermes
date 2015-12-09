import os

from configparser import ConfigParser

class ConfigSection(object):
    pass

class Config(object):
    """
    Configuration parser for evesp .conf files
    @author: Fabio Manganiello <blacklight86@gmail.com>
    """

    ######
    # Private methods
    ######

    __default_config_file_name = 'evesp.conf'
    __engine_section_name = 'engine'

    def __parse_rc_file(self, rcfile):
        parser = ConfigParser()
        self.components = {}

        with open(rcfile) as fp:
            parser.read_file(fp)

        for section in parser.sections():
            # Ignore sections having enabled = False
            if parser.has_option(section, 'enabled') and parser.getboolean(section, 'enabled') is False:
                continue

            # Two ways to access the Config parameters
            # 1: config.component_name.value
            # 2: config.components['component_name']['value']
            for key, value in parser.items(section):
                if not section in self.__dict__:
                    self.__dict__[section] = ConfigSection()

                    # "engine" is considered as a special section for engine configuration.
                    # Any other section is treated as a component
                    if section != self.__engine_section_name:
                        self.components[section] = {}

                self.__dict__[section].__dict__[key] = value
                self.components[section][key] = value

    def __get_conf_file_path(self):
        config_file_locations = [
            os.getcwd(),
            os.path.join(os.path.expanduser('~'), '.config', 'evesp'),
            os.path.join(os.path.abspath(os.sep), 'etc', 'evesp')
        ]

        for location in config_file_locations:
            rcfile = os.path.join(location, cls.__default_config_file_name)
            if os.path.isfile(rcfile):
                self.config_dir = location
                return rcfile

        raise RuntimeError('No valid configuration file was found - paths: %s' % config_file_locations)

    ######
    # Public methods
    ######

    def __init__(self, rcfile=None, **kwargs):
        """
        Configuration constructor

        rcfile -- Path string to the configuration file.
            If None, the Config object will be initialized on the basis of the kwargs named-values.
            If no keyword arguments are passed, try to parse the main configuration file from one
            of the following locations:

            1. ./evesp.conf
            2. ~/.config/evesp/evesp.conf
            3. /etc/evesp/evesp.conf

        Sections having enabled=False will be skipped
        """

        if rcfile is None:
            if len(dict(kwargs).keys()) > 0:
                self.__dict__.update(kwargs)
                return

            rcfile = self.__get_conf_file_path()
        self.__parse_rc_file(rcfile)

# vim:sw=4:ts=4:et:

