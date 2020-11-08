
def _strip_none(data):
    if isinstance(data, dict):
        return {k: _strip_none(v) for k, v in data.items() if k is not None and v is not None}
    elif isinstance(data, list):
        return [_strip_none(item) for item in data if item is not None]
    elif isinstance(data, tuple):
        return tuple(_strip_none(item) for item in data if item is not None)
    elif isinstance(data, set):
        return {_strip_none(item) for item in data if item is not None}
    else:
        return data


def fix_null_marshalling(func):
    """
    Intended to be applied around (above) the Flask-restplus decorator
    @api.marshal_with(...)

    See: https://github.com/noirbizarre/flask-restplus/issues/179
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return _strip_none(result)
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper