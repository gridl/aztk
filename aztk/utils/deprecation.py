import warnings
import functools
import inspect


def deprecated(reason: str = None):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    Args:
        reason (str): Reason to why this class or function is being deprecated
    """

    def decorator(func):
        if inspect.isclass(func):
            msg = "Call to deprecated class {name} ({reason})."
        else:
            msg = "Call to deprecated function {name} ({reason})."

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            deprecate(msg.format(func.__name__, reason))
            return func(*args, **kwargs)
        return new_func

    return decorator


def deprecate(message: str):
    """
    Print a deprecate warning.

    Args:
        message (str): Message to print
    """
    warnings.simplefilter('always', DeprecationWarning)  # turn off filter
    warnings.warn(message,
                  category=DeprecationWarning,
                  stacklevel=2)
    warnings.simplefilter('default', DeprecationWarning)  # reset filter
