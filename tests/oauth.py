# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import unittest
import h_annot.oauth

class TestOAuth(unittest.TestCase):

    def test_url(self):
        url = h_annot.api.oauth_url('client12345')
        self.assertEqual(url, 'https://hypothes.is/oauth/authorize?response_type=code&client_id=client12345')
        url = h_annot.api.oauth_url('client12345', 'state54321')
        self.assertEqual(url, 'https://hypothes.is/oauth/authorize?response_type=code&client_id=client12345&state=state54321')
        return

# eof
