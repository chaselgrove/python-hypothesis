# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import urllib
import requests

from .exceptions import *

server = 'https://hypothes.is'

def root():
    url = '%s/api' % server
    r = requests.get(url)
    if r.status_code != 200:
        raise APIError(r)
    return r.text

def search(auth, **kwargs):
    base_url = '%s/api/search' % server
    headers = {'Accept': 'application/json'}
    if auth:
        headers['Authorization'] = 'Bearer %s' % auth
    if not kwargs:
        url = base_url
    else:
        url = '%s?%s' % (base_url, urllib.urlencode(kwargs))
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise APIError(r)
    return r.text

def read(auth, annot_id):
    url = '%s/api/annotations/%s' % (server, annot_id)
    headers = {'Accept': 'application/json'}
    if auth:
        headers['Authorization'] = 'Bearer %s' % auth
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise APIError(r)
    return r.text

def create(auth, data):
    headers = {'Authorization': 'Bearer %s' % auth, 
               'Content-type': 'application/json;charset=UTF-8'}
    url = '%s/api/annotations' % server
    r = requests.post(url, headers=headers, data=data)
    if r.status_code != 200:
        raise APIError(r)
    return r.text

def update(auth, annot_id, data):
    headers = {'Authorization': 'Bearer %s' % auth, 
               'Content-type': 'application/json;charset=UTF-8'}
    url = '%s/api/annotations/%s' % (server, annot_id)
    r = requests.put(url, headers=headers, data=data)
    if r.status_code != 200:
        raise APIError(r)
    return r.text

def delete(auth, annot_id):
    url = '%s/api/annotations/%s' % (server, annot_id)
    headers = {'Authorization': 'Bearer %s' % auth}
    r = requests.delete(url, headers=headers)
    if r.status_code != 200:
        raise APIError(r)
    return r.text

# eof
