# See file COPYING distributed with python-hypothesis for copyright and 
# license.

# Some of the tests in this file are designed to check if the search 
# function is passing its parameters correctly to the Hypothesis API.  
# If no annotations are returned by the search, we can't check that the 
# filter has been applied properly, so we consider this an error because 
# the test can't do its job.  (We choose to trigger an error rather than 
# to skip the test so the problem is clear in the test output.)  These 
# errors are triggered by the exceptions in the setUp()s.

import itertools
import unittest
import h_annot.annotation
from . import config

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

class TestSearchResults(unittest.TestCase):

    def setUp(self):
        self.no_results = h_annot.search(uri='https://github.com/chaselgrove/python-hypothesis', text='this_annotation_should_not_exist', user='chaselgrove')
        self.some_results = h_annot.search(uri='https://github.com/chaselgrove/python-hypothesis', user='chaselgrove')
        self.all_results = h_annot.search()
        return

    def test_type(self):
        self.assertIsInstance(self.no_results, h_annot.annotation.SearchResults)
        self.assertIsInstance(self.some_results, h_annot.annotation.SearchResults)
        self.assertIsInstance(self.all_results, h_annot.annotation.SearchResults)
        return

    def test_len(self):
        self.assertEqual(len(self.no_results), 0)
        self.assertGreater(len(self.some_results), 0)
        self.assertLess(len(self.some_results), 10)
        self.assertGreater(len(self.all_results), 100000)
        return

    def test_iteration(self):
        # catch non-empty no_results and some_results here -- we don't really 
        # want to be iterating over all of the results if something goes 
        # wrong and there are thousands
        if len(self.no_results) != 0:
            raise ValueError('results found in no_results')
        if len(self.some_results) > 10:
            msg = 'more results than expected found in some_results'
            raise ValueError(msg)
        try:
            no_results_list = list(self.no_results)
            some_results_list = list(self.some_results)
        except Exception as exc:
            self.fail('list() failed on search results: %s' % exc)
        self.assertEqual(len(no_results_list), 0)
        self.assertEqual(len(some_results_list), len(self.some_results))
        annotation_checks = [ isinstance(res, h_annot.annotation.Annotation) 
                              for res in some_results_list ]
        self.assertTrue(all(annotation_checks))
        first_250_list = list(itertools.islice(self.all_results, 250))
        self.assertEqual(len(first_250_list), 250)
        annotation_checks = [ isinstance(res, h_annot.annotation.Annotation) 
                              for res in first_250_list ]
        self.assertTrue(all(annotation_checks))
        # make sure we really get new results, not duplicates
        annotation_ids = set(a.id for a in first_250_list)
        self.assertEqual(len(annotation_ids), 250)
        return

# eof
