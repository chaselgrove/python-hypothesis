import unittest
import json
import h_annot.api
from . import config

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

# eof
