import collections

from aztk.error import InvalidModelFieldError
from . import validators as aztk_validators

# pylint: disable=W0212
class Field:
    """
    Base class for all model fields
    """
    def __init__(self, *validators, **kwargs):
        self.default = kwargs.get('default')
        self.required = 'default' not in kwargs
        self.validators = []

        if self.required:
            self.validators.append(aztk_validators.Required())

        self.validators.extend(validators)

        choices = kwargs.get('choices')
        if choices:
            self.validators.append(aztk_validators.In(choices))

    def validate(self, value):
        for validator in self.validators:
            validator(value)

    def decode(self, value):
        if hasattr(self, "__decode__"):
            value = self.__decode__(value)

        return value

    def __get__(self, instance, owner):
        if instance is not None:
            try:
                return instance._data[self]
            except KeyError:
                return instance._data.setdefault(self, self._default(instance))

        return self

    def __set__(self, instance, value):
        instance._data[self] = value


    def _default(self, model):
        if callable(self.default):
            return self.__call_default(model)

        return self.default

    def __call_default(self, *args):
        try:
            return self.default()
        except TypeError as error:
            try:
                return self.default(*args)
            except TypeError:
                raise error


class String(Field):
    """
    Model String field
    """

    def __init__(self, *args, **kwargs):
        super().__init__(aztk_validators.String(), *args, **kwargs)


class Integer(Field):
    """
    Model Integer field
    """
    def __init__(self, *args, **kwargs):
        super().__init__(aztk_validators.Integer(), *args, **kwargs)


class Float(Field):
    """
    Model Float field
    """

    def __init__(self, *args, **kwargs):
        super().__init__(aztk_validators.Float(), *args, **kwargs)


class Boolean(Field):
    """
    Model Boolean field
    """

    def __init__(self, *args, **kwargs):
        super().__init__(aztk_validators.Boolean(), *args, **kwargs)


class List(Field):
    """
    Field that should be a list
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', list)

        super().__init__(
            aztk_validators.List(*kwargs.get('inner_validators', [])),
            *args, **kwargs)


class Model(Field):
    """
    Field is another model
    """

    def __init__(self, model, *args, **kwargs):
        super().__init__(aztk_validators.Model(model), *args, **kwargs)

        self.model = model

    def __set__(self, instance, value):
        if isinstance(value, collections.MutableMapping):
            value = self.model(**value)

        super().__set__(instance, value)

class Enum(Field):
    """
    Field that should be an enum
    """
    def __init__(self, model, *args, **kwargs):
        super().__init__(aztk_validators.InstanceOf(model), *args, **kwargs)

        self.model = model

    def __set__(self, instance, value):
        if not isinstance(value, self.model):
            try:
                value = self.model(value)
            except ValueError:
                available = [e.value for e in self.model]
                raise InvalidModelFieldError("{0} is not a valid option. Use one of {1}".format(value, available))
        super().__set__(instance, value)

