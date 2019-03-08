# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import six
import urllib
import requests
from .exceptions import *

server = 'https://hypothes.is'

def oauth_url(client_id, state=None):
    url = '%s/oauth/authorize?response_type=code&client_id=%s' % (server, client_id)
    if state:
        url = url + '&state=' + state
    return url

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
        if six.PY2:
            url = '%s?%s' % (base_url, urllib.urlencode(kwargs))
        else:
            url = '%s?%s' % (base_url, urllib.parse.urlencode(kwargs))
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

def profile(auth):
    url = '%s/api/profile' % server
    headers = {'Accept': 'application/json'}
    if auth:
        headers['Authorization'] = 'Bearer %s' % auth
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise APIError(r)
    return r.text

def oauth_token(client_id, client_secret=None, code=None):
    url = '%s/api/token' % server
    data = {'grant_type': 'authorization_code', 
            'client_id': client_id}
    if client_secret is not None:
        data['client_secret'] = client_secret
    if code is not None:
        data['code'] = code
    r = requests.post(url, data=data)
    return r.text

def refresh_oauth_token(refresh_token):
    url = '%s/api/token' % server
    data = {'grant_type': 'refresh_token', 
            'refresh_token': refresh_token}
    r = requests.post(url, data=data)
    return r.text

def revoke_oauth(token):
    url = '%s/oauth/revoke' % server
    data = {'token': token}
    requests.post(url, data=data)
    return

# eof
