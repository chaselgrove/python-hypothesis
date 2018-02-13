import os
import unittest
import json
import h_annot.api

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

# eof
