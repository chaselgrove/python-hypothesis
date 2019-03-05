# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import unittest
import json
import h_annot.api
from . import config
from . import utils

class TestAPI(unittest.TestCase):

    @config.server_test
    def test_root(self):
        data = h_annot.api.root()
        try:
            json.loads(data)
        except:
            self.fail('json.loads() failed')
        return

    @config.server_test
    @config.params('TestAnnotation:annotation_id')
    def test_read(self, annotation_id):
        data = h_annot.api.read(None, annotation_id)
        try:
            json.loads(data)
        except:
            self.fail('json.loads() failed')
        return

    @config.server_test
    def test_not_found(self):
        regexp = 'API call returned 404 \(Not Found\)'
        self.assertRaisesRegexp(h_annot.exceptions.APIError, 
                                regexp, 
                                h_annot.api.read, 
                                *(None, 'bogusannotationid'))
        return

    @config.server_test
    @config.params('TestAnnotation:search_tag', 'TestAnnotation:search_uri')
    def test_search(self, tag, uri):
        data = h_annot.api.search(None, 
                                  limit=2, 
                                  sort='updated', 
                                  order='asc', 
                                  tag=tag)
        try:
            obj = json.loads(data)
        except:
            self.fail('json.loads() failed')
        self.assertIn('total', obj)
        self.assertGreaterEqual(obj['total'], 2)
        self.assertIn('rows', obj)
        self.assertGreaterEqual(len(obj['rows']), 2)
        self.assertEqual(obj['rows'][0]['uri'], uri)
        return

    @config.server_test
    def test_profile(self):
        data = h_annot.api.profile(None)
        try:
            obj = json.loads(data)
        except:
            self.fail('json.loads() failed')
        self.assertIn('userid', obj)
        self.assertEqual(obj['userid'], None)
        return

    @config.server_test
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

    @config.server_test
    @config.oauth_test
    def test_oauth_flow(self, 
                        client_id, 
                        client_secret, 
                        username, 
                        password):
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
