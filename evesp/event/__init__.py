class Event(object):
    """
    Base class for events
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, component=None, **kwargs):
        """
        Constructor
        Params:
            kwargs -- key-value associations for the attributes of the object
        """

        self.__kwargs = kwargs
        self.component = component
        for attr, value in kwargs.items():
            self.__dict__[attr] = value

    def get(self, attr):
        " Get an event attribute by name. Return None if the attribute doesn't exist "
        return self.__kwargs[attr] if attr in self.__kwargs else None

    def serialize(self):
        " Serialize the event using pickle "
        import pickle
        return pickle.dumps(self)

    @classmethod
    def deserialize(cls, event):
        " Deserialize and return the event object using pickle "
        import pickle
        obj = pickle.loads(event)

        assert isinstance(obj, cls)
        return obj

    def to_json(self):
        " Serialize as JSON "
        import json
        attrs = self.__kwargs
        return json.dumps(attrs)

    @classmethod
    def from_json(cls, attrs):
        " Deserialize and initialize from JSON "
        import json
        attrs = dict(json.loads(attrs))
        return Event(**attrs)

# vim:sw=4:ts=4:et:

