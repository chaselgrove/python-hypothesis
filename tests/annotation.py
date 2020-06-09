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
        self.assertEqual(annot.text, 'I\'m imagining!')
        self.assertEqual(annot.uri, \
                         'https://github.com/chaselgrove/python-hypothesis')
        self.assertIn('TestTag', annot.tags)
        self.assertIn('TestTag2', annot.tags)
        return

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

class TestEdits(unittest.TestCase):

    @config.server_test
    @config.params('TestEdit:auth_token', 'TestEdit:annot_id')
    def setUp(self, auth_token, annot_id):
        self.auth_token = auth_token
        self.annot_id = annot_id
        self.annotation = h_annot.Annotation.load(self.annot_id, 
                                                  self.auth_token)
        if 'test text' in self.annotation.text:
            raise ValueError('"test text" is in the test annotation')
        if 'TestTag' in self.annotation.tags:
            raise ValueError('TestTag is in the test annotation tags')
        self.orig_text = self.annotation.text
        return

    def tearDown(self):
        self.annotation.text = self.orig_text
        if 'TestTag' in self.annotation.tags:
            self.annotation.tags.remove('TestTag')
        return

    def test_text(self):
        self.annotation.text = self.orig_text + '\n' + 'test text'
        self.assertIn('test text', self.annotation.text)
        reloaded_annotation = h_annot.Annotation.load(self.annot_id)
        self.assertIn('test text', reloaded_annotation.text)
        return

    def test_tags(self):
        self.assertNotIn('TestTag', self.annotation.tags)
        self.annotation.tags.add('TestTag')
        self.assertIn('TestTag', self.annotation.tags)
        reloaded_annotation = h_annot.Annotation.load(self.annot_id)
        self.assertIn('TestTag', reloaded_annotation.tags)
        self.annotation.tags.remove('TestTag')
        self.assertNotIn('TestTag', self.annotation.tags)
        reloaded_annotation = h_annot.Annotation.load(self.annot_id)
        self.assertNotIn('TestTag', reloaded_annotation.tags)
        self.assertRaises(KeyError, self.annotation.tags.remove, 'TestTag')
        return

    def test_text_update_auth_deprecation(self):
        if sys.version_info.major == 2:
            raise self.skipTest('skipping in Python 2')
        with warnings.catch_warnings(record=True) as w:
            self.annotation.text = self.orig_text + '\n' + 'test text'
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
        return

    def test_tags_update_auth_deprecation(self):
        if sys.version_info.major == 2:
            raise self.skipTest('skipping in Python 2')
        with warnings.catch_warnings(record=True) as w:
            self.annotation.tags.add('TestTag')
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
        return

class TestEditsCMAuth(unittest.TestCase):

    @config.server_test
    @config.params('TestEdit:auth_token', 'TestEdit:annot_id')
    def setUp(self, auth_token, annot_id):
        self.auth_token = auth_token
        self.annot_id = annot_id
        self.annotation = h_annot.Annotation.load(self.annot_id)
        if 'test text' in self.annotation.text:
            raise ValueError('"test text" is in the test annotation')
        if 'TestTag' in self.annotation.tags:
            raise ValueError('TestTag is in the test annotation tags')
        self.orig_text = self.annotation.text
        return

    def tearDown(self):
        with h_annot.auth(self.auth_token):
            self.annotation.text = self.orig_text
            if 'TestTag' in self.annotation.tags:
                self.annotation.tags.remove('TestTag')
        return

    def test_text(self):
        with h_annot.auth(self.auth_token):
            self.annotation.text = self.orig_text + '\n' + 'test text'
        self.assertIn('test text', self.annotation.text)
        reloaded_annotation = h_annot.Annotation.load(self.annot_id)
        self.assertIn('test text', reloaded_annotation.text)
        return

    def test_tags(self):
        self.assertNotIn('TestTag', self.annotation.tags)
        with h_annot.auth(self.auth_token):
            self.annotation.tags.add('TestTag')
        self.assertIn('TestTag', self.annotation.tags)
        reloaded_annotation = h_annot.Annotation.load(self.annot_id)
        self.assertIn('TestTag', reloaded_annotation.tags)
        with h_annot.auth(self.auth_token):
            self.annotation.tags.remove('TestTag')
        self.assertNotIn('TestTag', self.annotation.tags)
        reloaded_annotation = h_annot.Annotation.load(self.annot_id)
        self.assertNotIn('TestTag', reloaded_annotation.tags)
        self.assertRaises(KeyError, self.annotation.tags.remove, 'TestTag')
        return

class TestChangeURI(unittest.TestCase):

    @config.params('TestChangeURI:auth_token', 
                   'TestChangeURI:annot_id', 
                   'TestChangeURI:uri_i', 
                   'TestChangeURI:uri_f')
    def setUp(self, auth_token, annot_id, uri_i, uri_f):
        with h_annot.auth(auth_token):
            self.annotation = h_annot.Annotation.load(annot_id)
        self.uri_i = uri_i
        self.uri_f = uri_f
        return

    def tearDown(self):
        self.annotation.uri = self.uri_i
        return

    def test_change_uri(self):
        self.annotation.uri = self.uri_f
        annot2 = h_annot.Annotation.load(self.annotation.id)
        self.assertEqual(annot2.uri, self.uri_f)
        return

# eof
