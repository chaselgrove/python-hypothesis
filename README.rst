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

    >>> h_annot.api.read(None, 'v8Y0ix_lSRmDnEKhNr19eQ')
    u'{"updated": "2013-08-14T19:21:19.917589+00:00", "group": "__world__", ...

    >>> h_annot.api.read(None, 'bogusannotationid')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "h_annot/api.py", line 39, in read
        raise APIError(r)
    h_annot.exceptions.APIError: API call returned 404 (Not Found): not_found

High-level access
-----------------

The Annotation class is an object abstraction of an annotation.  Use the ``load()`` class method to get an annotation from its ID:

    >>> annot = h_annot.Annotation.load('v8Y0ix_lSRmDnEKhNr19eQ')
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

Some attributes can be updated, but you must declare your developer key to the annotation when you create it:

    >>> annot = h_annot.Annotation.load('someannotationid', 'somedevelkey')
    >>> annot.text = 'new text'

Tags are accessed and changed through the ``tags`` attribute.  This attribute acts like a case-insensitive set (like Hypothesis itself treats tags).

    >>> print annot.tags
    TagSet(objectives, interwebs)

    >>> for tag in annot.tags:
    ... print tag
    objectives
    interwebs

    >>> annot.tags = ['all', 'new', 'tags']
    >>> annot.tags.add('and one more')
