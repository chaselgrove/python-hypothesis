# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import six

if six.PY2:
    from annotation import Annotation
    import api
else:
    from .annotation import Annotation
    from . import api

def get_oauth_url(client_id, state=None):
    url = '%s/oauth/authorize?response_type=code&client_id=%s' % (api.server, client_id)
    if state:
        url = url + '&state=' + state
    return url

__version__ = '0.2.0'

# eof
