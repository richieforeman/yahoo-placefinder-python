__author__ = 'Richie Foreman <richie.foreman@gmail.com>'
from urllib import urlencode
import httplib2
import json

http = httplib2.Http()

_base_uri = "http://where.yahooapis.com/geocode"
_decode = json.loads

appid = "rofl"
locale = "en_US"

class NoResultsException(Exception):
    pass


def geocode(q=None, flags="JRT", gflags="AC", **kwargs):
    '''
        Geocode an address, accepts kwargs based upon params documented here:
        http://developer.yahoo.com/geo/placefinder/guide/requests.html
    '''
    # push q to the query arg dict.
    if q:
        kwargs["q"] = q

    # force JSON
    if "J" not in flags:
        flags = flags + "J"

    uri = _base_uri + "?appid=%s&flags=%s&gflags=%s&%s" % (appid, flags, gflags, urlencode(kwargs))

    # yahoo returns a 200 for everything..
    response, content = http.request(uri)
    content = _decode(content)

    if content["ResultSet"]["Found"] == 0:
        raise NoResultsException("Found 0 Results")
    else:
        return content["ResultSet"]["Results"]