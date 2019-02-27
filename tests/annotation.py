# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import unittest
import json
import h_annot
from . import config

class TestAnnotation(unittest.TestCase):

    @config.params('TestAnnotation:annotation_id')
    def test_read(self, annotation_id):
        annot = h_annot.Annotation.load(annotation_id)
        self.assertIsInstance(annot, h_annot.Annotation)

    def test_not_found(self):
        regexp = 'API call returned 404 \(Not Found\)'
        self.assertRaises(KeyError, 
                          h_annot.Annotation.load, 
                          'bogusannotationid')
        return

    def test_search(self):
        annots = h_annot.Annotation.search(limit=2, 
                                           sort='updated', 
                                           order='asc', 
                                           tag='PythonHypothesis')
        self.assertGreaterEqual(len(annots), 2)
        self.assertIsInstance(annots[0], h_annot.Annotation)
        uri = 'https://github.com/chaselgrove/python-hypothesis'
        self.assertEqual(annots[0].uri, uri)
        return

# eof
