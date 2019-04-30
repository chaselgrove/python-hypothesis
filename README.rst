.. See file COPYING distributed with python-hypothesis for copyright and 
   license.

Python package for Hypothesis (http://hypothes.is)
==================================================

This package provides python bindings to the Hypothesis API.

Low-level access
----------------

The api submodule is a low-level implementation of the `Hypothesis API`_.  

.. _Hypothesis API: http://h.readthedocs.io/en/latest/api/

The contents of this module reflect the REST nature of the API:

- API calls are made by functions.
- Input and output data are uninterpreted data (e.g. JSON strings, not 
  objects resulting from interpreting the JSON).
- Argument checking is minimal and most exceptions will come when the API 
  returns an error (APIError is raised if the server does not return 200).
- The ``auth`` argument is always given first (except to ``root()``, which 
  does not take authorization).  ``auth`` can currently be None or a string 
  containing a developer token.

Examples:

    >>> h_annot.api.read(None, '53LMZGVCEemN4zOvm3oFEQ')
    u'{"updated": "2019-04-22T21:09:23.352503+00:00", "group": "__world__", ...

    >>> h_annot.api.read(None, 'bogusannotationid')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "h_annot/api.py", line 39, in read
        raise APIError(r)
    h_annot.exceptions.APIError: API call returned 404 (Not Found): not_found

High-level access
-----------------

The Annotation class is an object abstraction of an annotation.  Use the ``load()`` class method to get an annotation from its ID:

    >>> annot = h_annot.Annotation.load('53LMZGVCEemN4zOvm3oFEQ')
    >>> annot.text
    u"I'm imagining!!!"

Exceptions are more pythonic:

    >>> h_annot.Annotation.load('somebogusannotid')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "h_annot/annotation.py", line 97, in load
        raise KeyError('annotation ID %s not found' % annot_id)
    KeyError: 'annotation ID somebogusannotid not found'

The Annotation constructor should not be called directly.

Some attributes can be updated; to do so, set the authentication token using the ``h_annot.auth()`` context manager:

    >>> with h_annot.auth(authentication_token):
    ...     annot.text = 'new text'

Annotations don't have an inherent concept of authentication, so the previous way of declaring authentication to annotations:

    >>> annot = h_annot.Annotation.load('someannotationid', 'somedevelkey')
    >>> annot.text = 'new text'

is deprecated.

Tags are accessed and changed through the ``tags`` attribute.  This attribute acts like a case-insensitive set (like Hypothesis itself treats tags).

    >>> print annot.tags
    TagSet(objectives, interwebs)

    >>> for tag in annot.tags:
    ...     print tag
    objectives
    interwebs

    >>> with h_annot.auth(authentication_token):
    ...     annot.tags = ['all', 'new', 'tags']
    ...     annot.tags.add('and one more')
    ...     annot.tags.remove('new')

Searching via ``Annotation.search()`` is deprecated.  This search just wrapped the results of ``api.search()`` in Annotation constructors, so ``api.search()`` should now be used for searches that used ``Annotation.search()``.  For a high-level search interface, use ``h_annot.search()``.  This takes keyword arguments ``uri``, ``user``, ``tags``, and ``text``.  Note that ``tags`` are joined by AND and separate words in ``text`` are joined by OR, which is the behavior of the `Hypothesis search API`_.  ``h_annot.search()`` respects the authentication set by the ``h_annot.auth()`` context manager.

.. _Hypothesis search API: https://h.readthedocs.io/en/latest/api-reference/#tag/annotations/paths/~1search/get
