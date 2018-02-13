import unittest
import json
import h_annot

class TestAnnotation(unittest.TestCase):

    def test_read(self):
        annot = h_annot.Annotation.load('v8Y0ix_lSRmDnEKhNr19eQ')
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
