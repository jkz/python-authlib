import urllib
import urlparse

from .errors import Error

######### Auth functions ##########
def tuples2querystring(params):
    """
    Take a list of 2-tuples and return the tuples joined by '&' with
    their elements joined by '='.
    """
    #TODO: maybe this should be urllib.urlencode and use some utf8 encoding
    return '&'.join(('='.join((k, v)) for k, v in params))

def _utf8_str(s):
    """Convert unicode to utf-8."""
    if isinstance(s, unicode):
        return s.encode("utf-8")
    else:
        return str(s)

def percent_encode(s):
    return urllib.quote(_utf8_str(s), '~')

def percent_encode_dict(d):
    return dict([map(percent_encode, (k, v)) for k, v in d.iteritems()])


######### AuthClient functions ##########
def split_header(header):
    """Turn Authorization: header into parameters."""
    params = {}
    parts = header.split(',')
    for param in parts:
        # Ignore realm parameter.
        if param.find('realm') > -1:
            continue
        # Remove whitespace.
        param = param.strip()
        # Split key-value.
        param_parts = param.split('=', 1)
        # Remove quotes and unescape the value.
        params[param_parts[0]] = urllib.unquote(param_parts[1].strip('\"'))
    return params

def split_headers(headers):
    if 'Authorization' not in headers:
        raise Error('No Authorization header')

    auth_header = headers['Authorization']

    # Check that the authorization header is OAuth.
    if not auth_header[:6] == 'OAuth ':
        raise Error('Non-OAuth Authorization')

    # Strip 'oauth_' from parameter name
    auth_header = auth_header[6:]
    try:
        # Get the parameters from the header.
        params = split_header(auth_header)
    except Exception:
        raise Error('Unable to parse OAuth parameters from Authorization header.')

    # Split params into oauth and non-oauth
    oauth_params = {}
    non_oauth_params = {}
    for key, val in params.iteritems():
      if key[:6] == 'oauth_':
          oauth_params[key] = val
      else:
          non_oauth_params[key] = val
    return oauth_params, non_oauth_params

