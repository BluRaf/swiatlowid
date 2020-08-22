plugins = dict()

def command(name):
    def command_wrap(func):
        plugins[name] = func
        return func
    return command_wrap

def scan(namespace):
    """ Scans the namespace for modules and imports them, to activate decorator
    """

    import importlib
    import pkgutil

    name = importlib.util.resolve_name(namespace, package=__package__)
    spec = importlib.util.find_spec(name)

    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for finder, name, ispkg in pkgutil.iter_modules(module.__path__):
            spec = finder.find_spec(name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)