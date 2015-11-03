#!/usr/bin/env python

class Event(object):
    """
    Base class for events
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, id, **kwargs):
        """
        Constructor
        Params:
            id -- Any object which supports or overrides the __eq__() function (int, double and string works too)
            kwargs -- Any dictionary-based parameters
        """

        assert id is not None
        self.__id = id
        self.__kwargs = kwargs
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def equals(self, event):
        " Return true if the ID of two events is identical "
        return self.__id.__eq__(event.__id)

    def get(self, attr):
        " Get an event attribute by name. Return None if the attribute doesn't exist "
        return self.__kwargs[attr] if attr in self.__kwargs else None

    def id(self):
        " Get the event ID "
        return self.__id

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
        attrs['id'] = self.__id
        return json.dumps(attrs)

    @classmethod
    def from_json(cls, attrs):
        " Deserialize and initialize from JSON "
        import json
        attrs = dict(json.loads(attrs))
        id = attrs.pop('id')
        return Event(id, **attrs)

