#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""wikigrab.py - Wiki Grabber"""

import urllib
import os
import os.path
import re
import dircache
import codecs

from BeautifulSoup import BeautifulSoup

class WikiPusherError(Exception):
    def __init__(self, name, value):
        self.value = value
        self.name = name

    def __str__(self):
        return self.name + ":" + repr(self.value)

class WikiPusher(object):
    """Wiki grabbing tool"""

    def __init__(self, config):
        """Constructor"""
        self._config = config


    def get_config(self, string):
        """get config value"""
        return self._config[string]


    def _read(self, pathname):
        f = codecs.open(pathname, "r", "utf-8")
        text = f.read()
        f.close()
        return text

    def callback(self, url, text):
        regex_list = [
            (r"\[\[(.*?)\|(.*?)\]\]",  r"[\1 \2]"),
            (r"\[\[(.*?)\]\]", r"[\1]"),
            (r"\*\*(.*?)\*\*", r"'''\1'''"),  # bold
            (r"http://", "http-+-"),
            (r"https://", "https-+-"),
            (r"//(.*?)//", r"''\1''"),  # italic
            (r"\\\\", r"[[BR]]"),
            (r"^======([^=].*?)======", r"= \1"),
            (r"^=====([^=].*?)=====", r"== \1"),
            (r"^====([^=].*?)====", r"=== \1"),
            (r"^===([^=].*?)===", r"==== \1"),
            (r"^==([^=].*?)==", r"===== \1"),
            (r"^=([^=].*?)=", r"====== \1"),
            (r"^\s+-\s(.*?)", r" 1. "),
            (r"\[(.*?):(.*?) (.*)\]", r"[\1-\2 \3]"),
            (r"(http|https)\-\+\-", r"\1://"),
            (r"&quot;", r'"'),
            ]

#        for (regex, subst) in regex_list:
#            text = re.sub(regex, subst, text)
#        print text
#        return text

        output = []
        for line in text.split("\n"):
            for (regex, subst) in regex_list:
                line = re.sub(regex, subst, line)
            output.append(line)

#        print "\n".join(output)
        return "\n".join(output)


    def run(self):
        """Run grubbber"""
        target_dir = self.get_config("dir")
        prefix = self.get_config("prefix")
        for file in dircache.listdir(target_dir):
            filepath = os.path.join(target_dir, file)

            print file, filepath
            if re.search(r"\.txt$", file):
                if os.path.isfile(filepath):
                    bodytext = self._read(filepath)

#                    file = file.replace("-", "/")
                    file = file.replace(".txt", "")
                    url = self.get_config("prefix") + file + "?action=update"
                    bodytext = self.callback(url, bodytext)
                    params = dict(textarea_height="24", text=bodytext, commit=u"保存", comment="")
                    print "post: %s" % (url,)
                    self.push_by_post(url, params)
            


    def check_config(self):
        """check config"""
        key_vital = ["prefix", "dir", "max_recur"]
        for key in key_vital:
            if not self._config.has_key(key):
                raise WikiPusherError("config_no_vital_key", key_vital)

    def push_by_post(self, url, params):
        """grab given url as local html by POST method"""
        for key in params:
            if isinstance(params[key], unicode):
                params[key] = params[key].encode("utf-8")
        encoded_params = urllib.urlencode(params)
        u = urllib.urlopen(url, encoded_params)
        data = u.read()
        return data


