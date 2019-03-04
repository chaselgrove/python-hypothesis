# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import contextlib
import six

if six.PY2:
    from annotation import Annotation
    import api
else:
    from .annotation import Annotation
    from . import api

@contextlib.contextmanager
def server(url):
    orig_server = api.server
    api.server = url
    try:
        yield
    finally:
        api.server = orig_server
    return

__version__ = '0.2.1'

# eof
