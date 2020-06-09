# See file COPYING distributed with python-hypothesis for copyright and 
# license.

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
import re
import requests
import h_annot

# This function performs the OAuth flow given a client ID, username,
# and password on the server currently defined in h_annot.api.server.
# This is cobbled together by reverse engineering an OAuth process
# at the time of writing and is therefore fragile to changes in the
# Hypothesis server.
def get_oauth_code(client_id, username, password):
    csrf_re = re.compile('<input.*name="csrf_token" value="([^"]*)"')
    url = h_annot.api.oauth_url(client_id)
    with requests.Session() as s:
        response = s.get(url)
        csrf_token = csrf_re.search(response.text).groups()[0]
        data = {'__formid__': (None, 'deform'),
                'csrf_token': (None, csrf_token), 
                'username': (None, username),
                'password': (None, password),
                'Log_in': (None, 'Log_in')}
        response = s.post(response.url, files=data)
        data = {'response_mode': 'None',
                'response_type': 'code',
                'client_id': client_id}
        response = s.post(response.url, data=data, allow_redirects=False)
        parsed_url = urlparse.urlparse(response.headers['Location'])
    return urlparse.parse_qs(parsed_url.query)['code'][0]

# eof
