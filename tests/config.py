# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import h_annot

config = configparser.ConfigParser()
try:
    config.read(os.environ['PYTHON_HYPOTHESIS_TESTS_CONFIG'])
except KeyError:
    config.read('tests.config')

def get(test_case, key):
    (section, option) = key.split(':')
    try:
        value = config.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        raise test_case.skipTest('%s not defined in test configuration' % key)
    return value

def params(*parameter_keys):
    def decorator(f):
        # test_case here is self in the method we're decorating
        def f2(test_case):
            parameters = (get(test_case, key) for key in parameter_keys)
            return f(test_case, *parameters)
        return f2
    return decorator

def oauth_test(f):
    def f2(test_case):
        client_id = get(test_case, 'OAuth:client_id')
        username = get(test_case, 'OAuth:username')
        password = get(test_case, 'OAuth:password')
        try:
            client_secret = config.get('OAuth', 'client_secret')
        except (configparser.NoSectionError, configparser.NoOptionError):
            client_secret = None
        return f(test_case, client_id, client_secret, username, password)
    return f2

def server_test(f):
    """applies General:server from the configuration file to the decorated 
    test
    """
    try:
        server = config.get('General', 'server')
    except (configparser.NoSectionError, configparser.NoOptionError):
        return f
    def f2(test_case, *args, **kwargs):
        with h_annot.server(server):
            return f(test_case, *args, **kwargs)
    return f2

# eof
