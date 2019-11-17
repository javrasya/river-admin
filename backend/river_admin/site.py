def _to_key(model_class, field_name):
    return model_class.__module__ + "." + model_class.__name__ + "." + field_name


class RiverAdmin(object):
    icon = None
    name = None
    list_displays = None

    def get_list_displays(self):
        return self.list_displays


class Site(object):
    def __init__(self):
        self._registry = {}

    def register(self, model_class, field_name, admin):
        self._registry[_to_key(model_class, field_name)] = admin

    def get(self, model_class, field_name):
        return self._registry.get(_to_key(model_class, field_name), None)
