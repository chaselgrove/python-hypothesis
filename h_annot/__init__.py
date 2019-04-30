# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import contextlib
import six

if six.PY2:
    from annotation import Annotation, search
    import api, oauth
else:
    from .annotation import Annotation, search
    from . import api, oauth

@contextlib.contextmanager
def server(url):
    orig_server = api.server
    api.server = url
    try:
        yield
    finally:
        api.server = orig_server
    return

@contextlib.contextmanager
def auth(token):
    orig_auth = annotation.cm_auth
    annotation.cm_auth = token
    try:
        yield
    finally:
        annotation.cm_auth = orig_auth
    return

__version__ = '0.4.0'

# eof
