"""
Contains all errors used in Aztk.
All error should inherit from `AztkError`
"""


class AztkError(Exception):
    pass

class ClusterNotReadyError(AztkError):
    pass

class AzureApiInitError(AztkError):
    pass

class InvalidPluginConfigurationError(AztkError):
    pass

class InvalidModelError(AztkError):
    def __init__(self, message: str, model):
        super().__init__()
        self.message = message
        self.model = model

    def __str__(self):
        return "{model} {message}".format(model=self.model, message=self.message)


class MissingRequiredAttributeError(InvalidModelError):
    pass

class InvalidCustomScriptError(InvalidModelError):
    pass

class InvalidPluginReferenceError(InvalidModelError):
    pass

class InvalidModelFieldError(InvalidModelError):
    def __init__(self, message: str, model = None, field = None):
        super().__init__(message, model)
        self.field = field

    def __str__(self):
        return "{model} {field} {message}".format(model=self.model, field=self.field, message=self.message)
