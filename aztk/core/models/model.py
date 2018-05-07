from aztk.error import InvalidModelError, InvalidModelFieldError

from aztk.core.models import fields

# pylint: disable=W0212
class ModelMeta(type):
    """
    Model Meta class. This takes all the class definition and build the attributes form all the fields definitions.
    """
    def __new__(mcs, name, bases, attrs):
        print("New model meta",name, attrs)
        attrs['_fields'] = {}

        for base in bases:
            if hasattr(base, '_fields'):
                for k, v in base._fields.items():
                    attrs['_fields'][k] = v
            for k, v in base.__dict__.items():
                if isinstance(v, fields.Field):
                    attrs['_fields'][k] = v

        for k, v in attrs.items():
            if isinstance(v, fields.Field):
                attrs['_fields'][k] = v

        return super().__new__(mcs, name, bases, attrs)

class Model(metaclass=ModelMeta):
    """
    Base class for all aztk models
    """

    def __new__(cls, *args, **kwargs):
        model = super().__new__(cls)
        model._data = {}
        return model

    def __init__(self, **kwargs):
        self._update(kwargs)

    def __getitem__(self, k):
        print("Fields", k, self._fields)
        if k not in self._fields:
            raise AttributeError(k)

        return getattr(self, k)

    def __setitem__(self, k, v):
        if k not in self._fields:
            raise AttributeError(k)

        setattr(self, k, v)

    def validate(self):
        """
        Validate the entire model
        """

        for name, field in self._fields.items():
            try:
                field.validate(getattr(self, name))
            except InvalidModelFieldError as e:
                e.field = name
                e.model = self
                raise e
            except InvalidModelError as e:
                e.model = self
                raise e

    def _update(self, values):
        for k, v in values.items():
            self[k] = v
