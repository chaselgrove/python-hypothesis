# See file COPYING distributed with python-hypothesis for copyright and 
# license.

# Some of the tests in this file are designed to check if the search 
# function is passing its parameters correctly to the Hypothesis API.  
# If no annotations are returned by the search, we can't check that the 
# filter has been applied properly, so we consider this an error because 
# the test can't do its job.  (We choose to trigger an error rather than 
# to skip the test so the problem is clear in the test output.)  These 
# errors are triggered by the exceptions in the setUp()s.

import unittest
import h_annot
from . import config

class TestSearch(unittest.TestCase):

    def test_search(self):
        annotations = h_annot.annotation.search()
        self.assertIsInstance(annotations, list)
        self.assertEqual(len(annotations), 200)
        annot_types_okay = [ isinstance(a, h_annot.annotation.Annotation) 
                             for a in annotations ]
        self.assertTrue(all(annot_types_okay))
        return

class TestSearchUser(unittest.TestCase):

    def setUp(self):
        self.user = 'acct:chaselgrove@hypothes.is'
        self.annotations = h_annot.annotation.search(user=self.user)
        if len(self.annotations) == 0:
            raise ValueError('no annotations for user %s found' % self.user)
        return

    def test_search_user(self):
        self.assertTrue(all(a.user == self.user for a in self.annotations))
        return

class TestSearchURI(unittest.TestCase):

    def setUp(self):
        self.uri = 'https://web.hypothes.is'
        self.annotations = h_annot.annotation.search(uri=self.uri)
        if len(self.annotations) == 0:
            raise ValueError('no annotations for URI %s found' % self.uri)
        return

    def test_search_uri(self):
        uris_okay = [ a.uri in (self.uri, self.uri+'/')
                      for a in self.annotations ]
        self.assertTrue(all(uris_okay))
        return

class TestSearchTags(unittest.TestCase):

    def setUp(self):
        self.tag = 'APITest'
        self.annotations = h_annot.annotation.search(tags=[self.tag])
        if len(self.annotations) == 0:
            raise ValueError('no annotations for tag %s found' % self.tag)
        return

    def test_search_tags(self):
        tags_okay = [ self.tag in a.tags for a in self.annotations ]
        self.assertTrue(all(tags_okay))
        return

class TestSearchText(unittest.TestCase):

    def setUp(self):
        self.text = 'imagining'
        self.annotations = h_annot.annotation.search(text=self.text)
        if len(self.annotations) == 0:
            raise ValueError('no annotations for tag %s found' % self.tag)
        return

    def test_search_tags(self):
        text_okay = [ self.text in a.text.lower() for a in self.annotations ]
        self.assertTrue(all(text_okay))
        return

class TestAuthenticatedSearch(unittest.TestCase):

    @config.server_test
    @config.params('TestSearch:auth_token', 'TestSearch:uri', 'TestSearch:text')
    def setUp(self, auth, uri, text):
        self.text = text
        public_annotations = h_annot.annotation.search(uri=uri, text=self.text)
        for annot in public_annotations:
            if self.text in annot.text:
                fmt = '"%s" is found in a public annotation on %s'
                raise ValueError(fmt % (self.text, uri))
        with h_annot.auth(auth):
            self.annotations = h_annot.annotation.search(uri=uri, 
                                                         text=self.text)
        return

    def test_authenticated_search(self):
        text_matches = [ self.text in a.text for a in self.annotations ]
        self.assertTrue(any(text_matches))
        return

# eof
