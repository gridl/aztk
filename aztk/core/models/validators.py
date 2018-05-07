import collections

from aztk.error import InvalidModelFieldError


class Validator:
    """
    Base class for a validator.
    To write your validator extend this class and implement the validate method.
    To raise an error raise  InvalidModelFieldError
    """
    def __call__(self, value):
        self.validate(value)

    def validate(self, value):
        raise NotImplementedError()



class Required(Validator):
    """
    Validate the field valiue is not `None`
    """

    def validate(self, value):
        if value is None:
            raise InvalidModelFieldError('is required')


class String(Validator):
    """
    Validate the value of the field is a `str`
    """

    def validate(self, value):
        if not isinstance(value, str):
            raise InvalidModelFieldError('should be a string')


class Integer(Validator):
    """
    Validate the value of the field is a `int`
    """

    def validate(self, value):
        if not isinstance(value, int):
            raise InvalidModelFieldError('should be an integer')


class Float(Validator):
    """
    Validate the value of the field is a `float`
    """

    def validate(self, value):
        if not isinstance(value, float):
            raise InvalidModelFieldError('should be a float')


class Boolean(Validator):
    """This validator forces fields values to be an instance of `bool`."""

    def validate(self, value):
        if not isinstance(value, bool):
            raise InvalidModelFieldError('should be a boolean')



class In(Validator):
    """
    Validate the field value is in the list of allowed choices
    """

    def __init__(self, choices):
        self.choices = choices

    def validate(self, value):
        if value not in self.choices:
            raise InvalidModelFieldError('should be in {}'.format(self.choices))

class InstanceOf(Validator):
    """
    Check if the field is an instance of the given type
    """

    def __init__(self, cls):
        self.type = cls

    def validate(self, value):
        if not isinstance(value, self.type):
            raise InvalidModelFieldError(
                "should be an instance of '{}'".format(self.type.__name__))


class Model(Validator):
    """
    Validate the field is a model
    """

    def __init__(self, model):
        self.model = model

    def validate(self, value):
        if not isinstance(value, self.model):
            raise InvalidModelFieldError(
                "should be an instance of '{}'".format(self.model.__name__))

        value.validate()


class List(Validator):
    """This validator forces field values to be a :keyword:`list`.
    Also a list of inner :mod:`validators` could be specified to validate
    each list element. For example, to validate a list of
    :class:`models.Model` you could do::
        books = fields.Field(validators.List(validators.Model(YourBookModel)))
    :param \*validators: A list of inner validators as possitional arguments.
    """

    def __init__(self, *validators):
        self.validators = validators

    def validate(self, value):
        if not isinstance(value, collections.MutableSequence):
            raise InvalidModelFieldError('should be a list')

        for i in value:
            for validator in self.validators:
                validator(i)

