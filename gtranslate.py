#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""gtranslate.py - Transrate text with Google AJAX Language API"""

import urllib
import json

def translate(text, f="en", t="ja"):
    """Translate input string by `Google AJAX Language API`_.

    .. _Google AJAX Language API: http://code.google.com/apis/ajaxlanguage/documentation/reference.html

        >>> translation(u"Hello.")
        u'\\u3053\\u3093\\u306b\\u3061\\u306f\\u3002'
        >>> translation(u"\\u3053\\u3093\\u306b\\u3061\\u306f\\u3002", f="ja", t="en")
        u'Hello.'
        >>> translation(u"Hello.", "foo", "bar")
        Traceback (most recent call last):
        ...
        IOError: invalid translation language pair
        >>>
    """
    # unicode -> string (utf8)
    # urlencode does not allow unicode.
    if isinstance(text, unicode):
        text = text.encode("utf8")

    # Access to Translation API
    data = {
        "q": text,
        "v": "1.0",
        "hl": "ja",
        "langpair": "%s|%s" % (f, t),
        }
    f = urllib.urlopen("http://ajax.googleapis.com/ajax/services/language/translate",
        urllib.urlencode(data))

    # Result
    ret = json.loads(f.read())

    if ret["responseStatus"] != 200:
        raise IOError(ret.get("responseDetails", ""))

    return ret["responseData"]["translatedText"]


