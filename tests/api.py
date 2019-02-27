# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import unittest
import json
import h_annot.api
from . import config
from . import utils

class TestAPI(unittest.TestCase):

    def test_root(self):
        data = h_annot.api.root()
        try:
            json.loads(data)
        except:
            self.fail('json.loads() failed')
        return

    def test_read(self):
        data = h_annot.api.read(None, 'v8Y0ix_lSRmDnEKhNr19eQ')
        try:
            json.loads(data)
        except:
            self.fail('json.loads() failed')
        return

    def test_not_found(self):
        regexp = 'API call returned 404 \(Not Found\)'
        self.assertRaisesRegexp(h_annot.exceptions.APIError, 
                                regexp, 
                                h_annot.api.read, 
                                *(None, 'bogusannotationid'))
        return

    def test_search(self):
        data = h_annot.api.search(None, 
                                  limit=2, 
                                  sort='updated', 
                                  order='asc', 
                                  tag='PythonHypothesis')
        try:
            obj = json.loads(data)
        except:
            self.fail('json.loads() failed')
        self.assertIn('total', obj)
        self.assertGreaterEqual(obj['total'], 2)
        self.assertIn('rows', obj)
        self.assertGreaterEqual(len(obj['rows']), 2)
        uri = 'https://github.com/chaselgrove/python-hypothesis'
        self.assertEqual(obj['rows'][0]['uri'], uri)
        return

    def test_profile(self):
        data = h_annot.api.profile(None)
        try:
            obj = json.loads(data)
        except:
            self.fail('json.loads() failed')
        self.assertIn('userid', obj)
        self.assertEqual(obj['userid'], None)
        return

    @config.params('TestAPI:auth_token', 'TestAPI:userid')
    def test_authenticated_profile(self, auth_token, userid):
        data = h_annot.api.profile(auth_token)
        try:
            obj = json.loads(data)
        except:
            self.fail('json.loads() failed')
        self.assertIn('userid', obj)
        self.assertEqual(obj['userid'], userid)
        return

    @config.params('TestAPI:oauth_server', 
                   'TestAPI:oauth_client_id', 
                   'TestAPI:oauth_client_secret', 
                   'TestAPI:oauth_username', 
                   'TestAPI:oauth_password')
    def test_oauth_flow(self, 
                        server, 
                        client_id, 
                        client_secret, 
                        username, 
                        password):
        with h_annot.server(server):
            code = utils.get_oauth_code(client_id, username, password)
            data = h_annot.api.oauth_token(client_id, client_secret, code)
            try:
                obj = json.loads(data)
            except:
                self.fail('json.loads() failed')
            self.assertIn('access_token', obj)
            self.assertIn('token_type', obj)
            self.assertIn('expires_in', obj)
            self.assertIn('refresh_token', obj)
            self.assertIn('scope', obj)
            data = h_annot.api.refresh_oauth_token(obj['refresh_token'])
            try:
                obj = json.loads(data)
            except:
                self.fail('json.loads() failed')
            self.assertIn('access_token', obj)
            self.assertIn('token_type', obj)
            self.assertIn('expires_in', obj)
            self.assertIn('refresh_token', obj)
            self.assertIn('scope', obj)
        return

# eof
