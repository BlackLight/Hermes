def component_class_by_module_name(module_name):
    module = __import__(module_name, ['*'])
    for module_token in module_name.split('.')[1:]:
        module = getattr(module, module_token)
    return getattr(module, main_class_name_from_module_name(module_name))

def main_class_name_from_module_name(module_name):
    """
    By convention, component module names have lowercase with underscore names,
    while their main classes have camel case names
    """
    import re
    return re.sub(r'(^|((?!^)_))([a-zA-Z])', lambda m: m.group(3).upper(), module_name.split('.')[-1])

