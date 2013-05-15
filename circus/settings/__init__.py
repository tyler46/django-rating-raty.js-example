from .base import *
try:
    from .local import *
except ImportError, exc:
    exc.args = tuple(['%s ( did you created your own local.py?)' %
                     exc.args[0]])
    raise exc
