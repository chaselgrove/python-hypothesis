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

def get_oauth_url(client_id, state=None):
    url = '%s/oauth/authorize?response_type=code&client_id=%s' % (api.server, client_id)
    if state:
        url = url + '&state=' + state
    return url

__version__ = '0.2.1'

# eof
