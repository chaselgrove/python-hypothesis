# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import six
import json
import time
import datetime
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

    @uri.setter
    def uri(self, value):
        if self._auth is None and cm_auth is None:
            raise AttributeError('can\'t set attribute (no authorization)')
        new_dict = dict(self._dict)
        new_dict['uri'] = value
        self._update(new_dict)
        return

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

class SearchResults:

    def __init__(self, **kwargs):
        try:
            self.auth = kwargs['auth']
            del kwargs['auth']
        except KeyError:
            self.auth = None
        self.initial_search_args = kwargs
        self._search()
        self.initial_data = self.data
        self.total = self.data['total']
        return

    def _search(self, first=True):
        search_args = dict(self.initial_search_args)
        if not first:
            time.sleep(1)
            sort_field = self.initial_search_args['sort']
            after = self.data['rows'][-1][sort_field]
            search_args['search_after'] = after
        search_args['limit'] = 200
        self.data = json.loads(api.search(self.auth, **search_args))
        return

    def __len__(self):
        return self.total

    def __iter__(self):
        self.data = self.initial_data
        self.index = 0
        return self

    def __next__(self):
        if self.index == 200:
            self._search(False)
            self.index = 0
        if self.index >= len(self.data['rows']):
            raise StopIteration
        annot = Annotation(None, self.data['rows'][self.index])
        self.index += 1
        return annot

    next = __next__

def search(uri=None, user=None, tags=None, text=None, sort='updated', order='desc', after=None, auth=None):
    """Search for annotations.

    Returns a SearchResults object.

    Supported arguments:

        uri
        user
        tags
        text

    sort, order, and after (for search_after) are also supported.
    """
    search_args = {}
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
    if not isinstance(sort, six.string_types):
        raise TypeError('sort must be a string')
    if sort not in ('created', 'updated', 'group', 'id', 'user'):
        raise ValueError('bad value for sort')
    search_args['sort'] = sort
    if not isinstance(order, six.string_types):
        raise TypeError('order must be a string')
    if order not in ('asc', 'desc'):
        raise ValueError('bad value for order')
    search_args['order'] = order
    if after is not None:
        if sort in ('group', 'id', 'user'):
            if not isinstance(after, six.string_types):
                raise TypeError('after must be a string for %s sorting' % sort)
        else:
            if not isinstance(after, datetime.datetime):
                msg = 'after must be a datetime instance for %s sorting' % sort
                raise TypeError(msg)
        search_args['search_after'] = after
    if auth is None:
        auth = cm_auth
    search_args['auth'] = auth
    return SearchResults(**search_args)

# eof
