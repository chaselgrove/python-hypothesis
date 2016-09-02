# See file COPYING distributed with python-hypothesis for copyright and 
# license.

class BaseException(Exception):

    """base class for hypothesis exceptions"""

class APIError(BaseException):

    """error in API call"""

    def __init__(self, response):
        self.response = response
        return

    def __str__(self):
        try:
            obj = self.response.json()
            reason = obj['reason']
        except:
            reason = self.response.text
        fmt = 'API call returned %d (%s): %s'
        return fmt % (self.response.status_code, self.response.reason, reason)

# eof
