# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import six
import json
import dateutil.parser
from . import api
from .exceptions import *

class Annotation(object):

    def __init__(self, auth, data):
        self._auth = auth
        self._set_from_json(data)
        return

    def __str__(self):
        return '<Hypothesis annotation %s>' % self.id

    def _set_from_json(self, data):
        self._dict = json.loads(data)
        return

    def _update(self, new_dict):
        data_in = json.dumps(new_dict)
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
        if self._auth is None:
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
        try:
            data = api.read(auth, annot_id)
        except APIError as data:
            if data.response.status_code == 404:
                raise KeyError('annotation ID %s not found' % annot_id)
            raise
        return cls(auth, data)

    @classmethod
    def search(cls, auth=None, **kwargs):
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
        if self._annotation._auth is None:
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

# eof
