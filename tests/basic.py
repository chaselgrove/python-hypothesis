import unittest
import h_annot.api

class TestBasics(unittest.TestCase):

    def test_server_context_manager(self):
        self.assertEqual(h_annot.api.server, 'https://hypothes.is')
        with h_annot.server('http://localhost:8000'):
            self.assertEqual(h_annot.api.server, 'http://localhost:8000')
        self.assertEqual(h_annot.api.server, 'https://hypothes.is')
        return

# eof
