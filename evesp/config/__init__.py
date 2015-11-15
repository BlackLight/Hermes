import os

from configparser import ConfigParser

class ConfigSection(object):
    pass

class Config(object):
    """
    Configuration parser for EVEsp .conf files
    @author: Fabio Manganiello <blacklight86@gmail.com>
    """

    ######
    # Private methods
    ######

    __default_config_file_name = 'evesp.conf'

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
                    self.components[section] = {}

                self.__dict__[section].__dict__[key] = value
                self.components[section][key] = value

    @classmethod
    def __get_conf_file_path(cls):
        config_file_locations = [
            os.path.join(os.getcwd(), cls.__default_config_file_name),
            os.path.join(os.path.expanduser('~'), '.config', 'evesp', cls.__default_config_file_name),
            os.path.join(os.path.abspath(os.sep), 'etc', 'evesp', cls.__default_config_file_name)
        ]

        for location in config_file_locations:
            if os.path.isfile(location):
                return location

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

