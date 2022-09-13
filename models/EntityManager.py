from collections import defaultdict
from collections.abc import Callable


class MetaManager:
    def __get__(self, obj, objtype):
        if obj is None:
            return Manager(objtype)
        else:
            raise AttributeError(
                "Manger isn't accessible via {} instances".format(objtype)
            )


class Manager:
    _store = defaultdict(list)

    def __init__(self, client):
        self._client = client
        self._client_name = "{}.{}".format(client.__module__, client.__qualname__)

    def create(self, **kwargs):
        self._store[self._client_name].append(self._client(**kwargs))

    def all(self):
        return (obj for obj in self._store[self._client_name])

    def filter(self, a_lambda):
        if a_lambda.__code__.co_name != "<lambda>":
            raise ValueError("a lambda required")

        return (
            obj
            for obj in self._store[self._client_name]

            if eval(a_lambda.__code__, vars(obj).copy())
        )


class Model:
    objects = MetaManager()

    def __init__(self, **kwargs):
        if type(self) is Model:
            raise NotImplementedError

        class_attrs = self.__get_class_attributes(type(self))

        self.__init_instance(class_attrs, kwargs)

    def __get_class_attributes(self, cls):
        attrs = vars(cls)
        if "objects" in attrs:
            raise AttributeError(
                'class {} has an attribute named "objects" of type "{}"'.format(
                    type(self), type(attrs["objects"])
                )
            )
        attrs = {
            attr: obj
            for attr, obj in vars(cls).items()
            if not attr.startswith("_") and not isinstance(obj, Callable)
        }
        return attrs

    def __init_instance(self, attrs, kwargs_dict):
        for key, item in kwargs_dict.items():
            if key not in attrs:
                raise TypeError('Got an unexpected key word argument "{}"'.format(key))
            if isinstance(item, type(attrs[key])):
                setattr(self, key, item)
            else:
                raise TypeError(
                    "Expected type {}, got {}".format(type(attrs[key]), type(item))
                )
