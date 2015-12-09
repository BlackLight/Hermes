def camelize(module_name):
    " Turn an underscore-like module_name into a camelized ClassName "
    import re
    return re.sub(r'(^|((?!^)_))([a-zA-Z])', lambda m: m.group(3).upper(), module_name.split('.')[-1])

def uncamelize(class_name):
    " Turn a camelized ClassName into an underscore-like module_name "
    import re

    return re.sub(r'(^|[a-z])([A-Z])', lambda m: '%s%s%s' % (
        m.group(1),
        ('_' if len(m.group(1)) else ''),
        m.group(2).lower()
    ), class_name)

def component_class_by_module_name(module_name):
    " Get a component class given its module name "
    module = __import__(module_name, ['*'])
    for module_token in module_name.split('.')[1:]:
        module = getattr(module, module_token)
    return getattr(module, camelize(module_name))

def event_class_by_class_name(class_name):
    " Get an event class object given its class name "
    module_name = '.'.join([
        'evesp', 'event', uncamelize(class_name)
    ])

    module = __import__(module_name, ['*'])
    for module_token in module_name.split('.')[1:]:
        module = getattr(module, module_token)
    return getattr(module, class_name)

def action_class_by_class_name(class_name):
    " Get an action class object given its class name "
    module_name = '.'.join([
        'evesp', 'action', uncamelize(class_name)
    ])

    module = __import__(module_name, ['*'])
    for module_token in module_name.split('.')[1:]:
        module = getattr(module, module_token)
    return getattr(module, class_name)

def get_full_class_name(obj):
    " Get the full class name of an object, included its full module name "
    import inspect
    return inspect.getmodule(obj.__class__).__name__ + '.' + obj.__class__.__name__

# vim:sw=4:ts=4:et:

