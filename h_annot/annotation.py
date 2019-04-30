# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import six
import json
import dateutil.parser
import warnings
from . import api
from .exceptions import *

cm_auth = None

class Annotation(object):

    def __init__(self, auth, data):
        self._auth = auth
        if isinstance(data, dict):
            self._dict = data
        else:
            self._set_from_json(data)
        return

    def __str__(self):
        return '<Hypothesis annotation %s>' % self.id

    def _set_from_json(self, data):
        self._dict = json.loads(data)
        return

    def _update(self, new_dict):
        data_in = json.dumps(new_dict)
        if cm_auth:
            data_out = api.update(cm_auth, self.id, data_in)
        else:
            msg = 'Updating annotations without the authorization ' + \
                  'context manager (h_annot.auth()) is deprecated.'
            warnings.warn(msg, DeprecationWarning)
            data_out = api.update(self._auth, self.id, data_in)
        self._set_from_json(data_out)
        return

    @property
    def id(self):
        return self._dict['id']

    @property
    def created(self):
        return dateutil.parser.parse(self._dict['created'])

    @property
    def group(self):
        return self._dict['group']

    @property
    def permissions(self):
        return self._dict['permissions']

    @property
    def document(self):
        return self._dict['document']

    @property
    def target(self):
        return self._dict['target']

    @property
    def links(self):
        return self._dict['links']

    @property
    def tags(self):
        return TagSet(self)

    @tags.setter
    def tags(self, value):
        self.tags.set(value)
        return

    @property
    def text(self):
        return self._dict['text']

    @text.setter
    def text(self, value):
        if self._auth is None and cm_auth is None:
            raise AttributeError('can\'t set attribute (no authorization)')
        new_dict = dict(self._dict)
        new_dict['text'] = value
        self._update(new_dict)
        return

    @property
    def uri(self):
        return self._dict['uri']

    @property
    def updated(self):
        return dateutil.parser.parse(self._dict['updated'])

    @property
    def user(self):
        return self._dict['user']

    @classmethod
    def load(cls, annot_id, auth=None):
        if auth is None:
            auth = cm_auth
        try:
            data = api.read(auth, annot_id)
        except APIError as data:
            if data.response.status_code == 404:
                raise KeyError('annotation ID %s not found' % annot_id)
            raise
        return cls(auth, data)

    @classmethod
    def search(cls, auth=None, **kwargs):
        msg = 'Annotation.search() is deprecated.  Use ' + \
              'annotation.search() or api.seach() instead.'
        warnings.warn(msg, DeprecationWarning)
        if auth is None:
            auth = cm_auth
        data = api.search(auth, **kwargs)
        obj = json.loads(data)
        rv = [ cls(auth, json.dumps(row)) for row in obj['rows'] ]
        return rv

    @classmethod
    def create(cls, auth, title, tags, text, uri):
        obj = {'document': {'title': title}, 
               'tags': tags, 
               'text': text, 
               'uri': uri}
        if not auth:
            auth = cm_auth
        data = api.create(auth, json.dumps(obj))
        return cls(auth, data)

class TagSet:

    def __init__(self, annotation):
        self._annotation = annotation
        return

    def __str__(self):
        tag_string = ', '.join(self)
        return 'TagSet(%s)' % tag_string

    def __iter__(self):
        for tag in self._annotation._dict['tags']:
            yield tag
        return

    def __contains__(self, tag):
        tag = tag.lower()
        for t in self:
            if t.lower() == tag:
                return True
        return False

    def set(self, tags):
        if self._annotation._auth is None and cm_auth is None:
            raise AttributeError('can\'t set attribute (no authorization)')
        if not isinstance(tags, (tuple, list)):
            msg = 'direct assignment to tags must be from a tuple or list'
            raise TypeError(msg)
        new_dict = dict(self._annotation._dict)
        new_dict['tags'] = tags
        self._annotation._update(new_dict)
        return

    def add(self, tag):
        if tag in self:
            return
        tags = list(self)
        tags.append(tag)
        self.set(tags)
        return

    def remove(self, tag):
        if tag not in self:
            raise KeyError(tag)
        tags = list(self)
        for t in tags:
            if t.lower() == tag.lower():
                tags.remove(t)
                break
        self.set(tags)
        return

def search(uri=None, user=None, tags=None, text=None, auth=None):
    """Search for annotations.

    Returns a list of annotations.

    Supported arguments:

        uri
        user
        tags
        text

    Currently limits the number of returned annotations to 200.
    """
    search_args = {'sort': 'id', 'order': 'asc', 'limit': 200}
    if uri is not None:
        if not isinstance(uri, six.string_types):
            raise TypeError('uri must be a string')
        search_args['uri'] = uri
    if user is not None:
        if not isinstance(user, six.string_types):
            raise TypeError('user must be a string')
        search_args['user'] = user
    if tags is not None:
        if not isinstance(tags, list):
            raise TypeError('tags must be a list of strings')
        if not all(isinstance(tag, six.string_types) for tag in tags):
            raise TypeError('tags must be a list of strings')
        search_args['tags'] = '[%s]' % ','.join(tags)
    if text is not None:
        if not isinstance(text, six.string_types):
            raise TypeError('text must be a string')
        search_args['text'] = '"%s"' % text
    if auth is None:
        auth = cm_auth
    data = json.loads(api.search(auth, **search_args))
    return [ Annotation(None, row) for row in data['rows'] ]

# eof
