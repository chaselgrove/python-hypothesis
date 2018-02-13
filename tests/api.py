import os
import unittest
import json
import h_annot.api

class TestRoot(unittest.TestCase):

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

# eof
