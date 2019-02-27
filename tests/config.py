# See file COPYING distributed with python-hypothesis for copyright and 
# license.

import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

config = configparser.ConfigParser()
try:
    config.read(['tests.config', os.environ['PYTHON_HYPOTHESIS_TESTS_CONFIG']])
except KeyError:
    config.read(['tests.config'])

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

# eof
