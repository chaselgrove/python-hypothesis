# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import datetime
import json
from . import api

class OAuthClient(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        return

    def auth_url(self, state=None):
        return api.oauth_url(self.client_id, state)

    def get_credentials(self, code):
        data = api.oauth_token(self.client_id, self.client_secret, code)
        obj = json.loads(data)
        dt = datetime.timedelta(seconds=obj['expires_in'])
        return OAuthCredentials(obj['access_token'], 
                                obj['token_type'], 
                                obj['scope'], 
                                datetime.datetime.now() + dt, 
                                obj['refresh_token'])

class OAuthCredentials(object):

    def __init__(self, *args):
        if len(args) == 1:
            self._load_from_json(args[0])
        else:
            (access_token, token_type, scope, expires, refresh_token) = args
            self.access_token = access_token
            self.token_type = token_type
            self.scope = scope
            self.expires = expires
            self.refresh_token = refresh_token
        self.revoked = False
        return

    def _load_from_json(self, data):
        obj = json.loads(data)
        self.access_token = obj['access_token']
        dt = datetime.timedelta(seconds=obj['expires_in'])
        self.token_type = obj['token_type']
        self.scope = obj['scope']
        self.expires = datetime.datetime.now() + dt
        self.refresh_token = obj['refresh_token']
        return

    def refresh(self):
        self._load_from_json(api.refresh_oauth_token(self.refresh_token))
        return

    def revoke(self):
        api.revoke_oauth(self.access_token)
        self.access_token = None
        self.token_type = None
        self.scope = None
        self.expires = None
        self.refresh_token = None
        self.revoked = True
        return

# eof
