# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import unittest
import h_annot.oauth
from . import config, utils

class TestOAuthBasics(unittest.TestCase):

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

class TestOAuth(unittest.TestCase):

    @config.server_test
    @config.oauth_test
    def setUp(self, client_id, client_secret, username, password):
        self.client = h_annot.oauth.OAuthClient(client_id, client_secret)
        self.code = utils.get_oauth_code(client_id, username, password)
        self.creds = self.client.get_credentials(self.code)
        return

    @config.server_test
    def test_oauth_credentials(self):
        self.assertIsInstance(self.creds, h_annot.oauth.OAuthCredentials)
        return

    @config.server_test
    def test_refresh_credentials(self):
        access_token_0 = self.creds.access_token
        expires_0 = self.creds.expires
        refresh_token_0 = self.creds.refresh_token
        self.creds.refresh()
        self.assertNotEqual(self.creds.access_token, access_token_0)
        self.assertNotEqual(self.creds.refresh_token, refresh_token_0)
        self.assertGreater(self.creds.expires, expires_0)
        return

    @config.server_test
    def test_revoke_credentials(self):
        self.assertFalse(self.creds.revoked)
        self.creds.revoke()
        self.assertTrue(self.creds.revoked)
        self.assertIsNone(self.creds.access_token)
        self.assertIsNone(self.creds.token_type)
        self.assertIsNone(self.creds.scope)
        self.assertIsNone(self.creds.expires)
        self.assertIsNone(self.creds.refresh_token)
        return

# eof
