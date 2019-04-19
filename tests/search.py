# See file COPYING distributed with python-hypothesis for copyright and 
# license.

# Some of the tests in this file are designed to check if the search 
# function is passing its parameters correctly to the Hypothesis API.  
# If no annotations are returned by the search, we can't check that the 
# filter has been applied properly, so we consider this an error because 
# the test can't do its job.  (We choose to trigger an error rather than 
# to skip the test so the problem is clear in the test output.)  These 
# errors are triggered by the assertions in the setUp()s.

import unittest
import h_annot

class TestSearch(unittest.TestCase):

    def test_search(self):
        annotations = h_annot.annotation.search(None)
        self.assertIsInstance(annotations, list)
        self.assertEqual(len(annotations), 200)
        annot_types_okay = [ isinstance(a, h_annot.annotation.Annotation) 
                             for a in annotations ]
        self.assertTrue(all(annot_types_okay))
        return

class TestSearchUser(unittest.TestCase):

    def setUp(self):
        self.user = 'acct:chaselgrove@hypothes.is'
        self.annotations = h_annot.annotation.search(None, user=self.user)
        assert len(self.annotations) > 0, \
                'no annotations for user %s found' % self.user
        return

    def test_search_user(self):
        self.assertTrue(all(a.user == self.user for a in self.annotations))
        return

class TestSearchURI(unittest.TestCase):

    def setUp(self):
        self.uri = 'https://web.hypothes.is'
        self.annotations = h_annot.annotation.search(None, uri=self.uri)
        assert len(self.annotations) > 0, \
                'no annotations for URI %s found' % self.uri
        return

    def test_search_uri(self):
        uris_okay = [ a.uri in (self.uri, self.uri+'/')
                      for a in self.annotations ]
        self.assertTrue(all(uris_okay))
        return

class TestSearchTags(unittest.TestCase):

    def setUp(self):
        self.tag = 'APITest'
        self.annotations = h_annot.annotation.search(None, tags=[self.tag])
        assert len(self.annotations) > 0, \
                'no annotations for tag %s found' % self.tag
        return

    def test_search_tags(self):
        tags_okay = [ self.tag in a.tags for a in self.annotations ]
        self.assertTrue(all(tags_okay))
        return

# eof
