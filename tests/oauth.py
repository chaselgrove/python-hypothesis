# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import unittest
import h_annot.oauth
from . import config, utils

class TestOAuth(unittest.TestCase):

    def test_url(self):
        url = h_annot.api.oauth_url('client12345')
        self.assertEqual(url, 'https://hypothes.is/oauth/authorize?response_type=code&client_id=client12345')
        url = h_annot.api.oauth_url('client12345', 'state54321')
        self.assertEqual(url, 'https://hypothes.is/oauth/authorize?response_type=code&client_id=client12345&state=state54321')
        return

    def test_auth_url(self):
        client = h_annot.oauth.OAuthClient('client12345', 'secret24680')
        self.assertEqual(client.auth_url('state54321'), 'https://hypothes.is/oauth/authorize?response_type=code&client_id=client12345&state=state54321')
        return

    def test_auth_url_no_state(self):
        client = h_annot.oauth.OAuthClient('client12345', 'secret24680')
        self.assertEqual(client.auth_url(), 'https://hypothes.is/oauth/authorize?response_type=code&client_id=client12345')
        return

    @config.oauth_test
    def test_oauth_credentials(self, 
                               server, 
                               client_id, 
                               client_secret, 
                               username, 
                               password):
        client = h_annot.oauth.OAuthClient(client_id, client_secret)
        with h_annot.server(server):
            code = utils.get_oauth_code(client_id, username, password)
            creds = client.get_credentials(code)
            self.assertIsInstance(creds, h_annot.oauth.OAuthCredentials)
        return

# eof
