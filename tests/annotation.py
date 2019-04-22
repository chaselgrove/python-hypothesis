# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import sys
import unittest
import json
import warnings
import h_annot
from . import config

class TestAnnotation(unittest.TestCase):

    @config.server_test
    @config.params('TestAnnotation:annotation_id')
    def test_read(self, annotation_id):
        annot = h_annot.Annotation.load(annotation_id)
        self.assertIsInstance(annot, h_annot.Annotation)

    @config.server_test
    def test_not_found(self):
        self.assertRaises(KeyError, 
                          h_annot.Annotation.load, 
                          'bogusannotationid')
        return

    @config.server_test
    @config.params('TestAnnotation:search_tag', 'TestAnnotation:search_uri')
    def test_search(self, tag, uri):
        annots = h_annot.Annotation.search(limit=2, 
                                           sort='updated', 
                                           order='asc', 
                                           tag=tag)
        self.assertGreaterEqual(len(annots), 2)
        self.assertIsInstance(annots[0], h_annot.Annotation)
        self.assertEqual(annots[0].uri, uri)
        return

    @config.server_test
    @config.params('TestAnnotation:search_tag', 'TestAnnotation:search_uri')
    def test_search_deprecation_warning(self, tag, uri):
        if sys.version_info.major == 2:
            raise self.skipTest('skipping in Python 2')
        with warnings.catch_warnings(record=True) as w:
            h_annot.Annotation.search(limit=2, tag=tag)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
        return

# eof
