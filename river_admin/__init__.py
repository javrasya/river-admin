from river_admin.site import Site


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(instance) if instance else self.getter(owner)


DEFAULT_ADMIN_ICON = "mdi-sitemap"


class RiverAdmin(object):
    icon = None
    name = None
    list_displays = None
    _model_class = None
    _field_name = None

    def get_list_displays(self):
        return self.list_displays

    @classproperty
    def admin_name(cls):
        return cls.name or "%s (%s)" % (cls._model_class.__name__, cls._field_name)

    @classproperty
    def admin_icon(cls):
        return cls.icon or DEFAULT_ADMIN_ICON

    @classproperty
    def admin_list_displays(cls):
        return cls.list_displays or ["pk", cls._field_name]

    @classmethod
    def get_objects(cls):
        headers = cls.admin_list_displays
        for obj in cls._model_class.objects.all():
            yield dict({key: str(cls._get_value(obj, key)) for key in headers}, **cls._get_default_values(obj))

    @classmethod
    def _get_default_values(cls, obj):
        return {"id": obj.pk, "__str": str(obj)}

    @classmethod
    def _get_value(cls, obj, field):
        if hasattr(cls, field) and callable(getattr(cls, field)):
            return getattr(cls, field)(obj)
        else:
            return getattr(obj, field)


class DefaultRiverAdmin(RiverAdmin):

    @classmethod
    def of(cls, model_class, field_name):
        cls._model_class = model_class
        cls._field_name = field_name
        return cls


site = Site()
