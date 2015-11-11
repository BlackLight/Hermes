from configparser import ConfigParser

class Config(object):
    """
    Configuration parser for EVEsp .conf files
    @author: Fabio Manganiello <blacklight86@gmail.com>
    """

    ######
    # Private methods
    ######

    def __parse_rc_file(self, rcfile):
        parser = ConfigParser()
        with open(rcfile) as fp:
            parser.read_file(fp)

        for section in parser.sections():
            # Ignore sections having enabled = False
            if parser.has_option(section, 'enabled') and parser.getboolean(section, 'enabled') is False:
                continue

            """
            (Key) case insensitive flat mapping
            [logger]
            Level=INFO
            MyModule.level=DEBUG

            becomes

            self.config['logger.level'] = 'INFO'
            self.config['logger.mymodule.level'] = 'DEBUG'
            """
            for key, value in parser.items(section):
                key = ('%s.%s' % (section, key)).lower()
                self.config[key] = value

    ######
    # Public methods
    ######

    def __init__(self, rcfile):
        """
        Configuration constructor
        rcfile -- Path string to the configuration file
        """

        self.config = {}
        self.__parse_rc_file(rcfile)

        if len(self.config.items()) == 0:
            raise RuntimeError(
                'No configuration has been loaded - empty of invalid %s file'
                % (rcfile)
            )

    def get(self, attr):
        """
        Configuration getter
        attr -- Attribute name - note that we are case insensitive when it comes to attribute names
        """
        attr = attr.lower()
        # Let's agree on one thing:
        # A non-existing attribute is the same of an attribute having value None
        return self.config[attr] if attr in self.config else None

# vim:sw=4:ts=4:et:

