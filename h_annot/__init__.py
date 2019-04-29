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
def auth(url):
    orig_auth = annotation.auth
    annotation.auth = url
    try:
        yield
    finally:
        annotation.auth = orig_auth
    return

__version__ = '0.3.0'

# eof
