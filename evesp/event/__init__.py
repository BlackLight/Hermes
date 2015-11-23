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
        vars(self).update(kwargs)

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

    def __eq__(self, event):
        """
        Return true if event equals self.
        Two events are considered "equal" if:

        - Their types are the same, or one is a direct subclass of the other;
        - All of their constructor parameters are equal, unless a certain attribute is an instance of AttributeValueAny.
        """

        if not self.__same_classes(self, event):
            return False

        for (attr, value) in self.__kwargs.items():
            if not self.__same_values(value, event.__kwargs[attr]):
                return False
        return True

    @classmethod
    def __same_classes(cls, obj1, obj2):
        return type(obj1) == type(obj2)

    @classmethod
    def __same_values(cls, value1, value2):
        if not cls.__same_classes(value1, value2) \
                and not isinstance(value1, AttributeValueAny) \
                and not isinstance(value2, AttributeValueAny):
            return False
        return value1 == value2

class AttributeValueAny(object):
    """
    When an event attribute type is AttributeValueAny,
    that attribute won't be taken into account when
    two events are compared through == operator or
    explicit __eq__ method invocation.

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __eq__(self, value):
        """ Always return True. Any value equals "any" """
        return True

# vim:sw=4:ts=4:et:

