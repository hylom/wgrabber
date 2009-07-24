#!/usr/bin/env python
#

"""wikigrab.py - Wiki Grabber"""

import urllib
import os
import os.path
import re
from BeautifulSoup import BeautifulSoup

class WikiGrabberError(Exception):
    def __init__(self, name, value):
        self.value = value
        self.name = name

    def __str__(self):
        return self.name + ":" + repr(self.value)

class WikiGrabber(object):
    """Wiki grabbing tool"""

    def __init__(self, config):
        """Constructor"""
        self._config = config
        self._targets = {}
        self._url_lists = []


    def get_config(self, string):
        """get config value"""
        return self._config[string]


    def run(self):
        """Run grubbber"""

        self.check_config()

        if not os.path.isdir(self.get_config("output_dir")):
            raise WikiGrabberError("output_dir_not_exists", self.get_config("output_dir"))

        self._append_download_list(self.get_config("start_url"))
        """download html recursive"""

        url = self._get_next_download_url()
        while(url):

            # get html from url
            print "getting %s ..." % (url,)
            html = self.grab_by_get(url)
            output_path = self.get_config("output_dir") + "/" + url.replace(self.get_config("prefix"), "", 1)
            if output_path[-1] == "/":
               output_path = output_path + "__index__"

            for (target, char) in self.get_config("filename_subst_rule"):
                output_path = output_path.replace(target, char)

            self._create_dir_from_output_pathname(output_path)
            f = open(output_path, "w")
            f.write(html)
            f.close()

            # extract links from html
            anchors = self.extract_anchors(html, url)
            for anchor in anchors:
                self._append_download_list(anchor)
        
            # next
            url = self._get_next_download_url()


    def _create_dir_from_output_pathname(self, path):
        """create subdirectory for output file."""
        file_pathes = path.split("/")
        del file_pathes[-1]

        real_path = os.path.join(*file_pathes)
        # print "mkdir: %s \n" % (real_path,)
        if not os.path.isdir(real_path):
            os.makedirs(real_path)


    def _append_download_list(self, url):
        """append url to download list"""

        url = self._rewrite_url(url)
        if not self._check_url(url):
            return
        if not self._targets.has_key(url):
            self._targets[url] = 1
            self._url_lists.append(url)


    def _rewrite_url(self, url):
        """rewrite url"""
        for (rule, str) in self.get_config("rewrite_rule"):
            url = re.sub(rule, str, url)
        return url

    def _check_url(self, url):
        """filter url. if filterd, return blank string. default rule is allow-deny."""
        for rule in self.get_config("allow_rule"):
            if re.search(rule, url):
                break
            else:
                return False

        for rule in self.get_config("deny_rule"):
            if re.search(rule, url):
                return False

        return True

    def _get_next_download_url(self):
        if len(self._url_lists) == 0:
            return ""
        return self._url_lists.pop(0)
        

    def check_config(self):
        """check config"""
        key_vital = ["start_url", "prefix", "output_dir", "max_recur"]
        for key in key_vital:
            if not self._config.has_key(key):
                raise WikiGrabberError("config_no_vital_key", key_vital)
            

    def grab_by_get(self, url):
        """grab given url as local html by GET method"""
        u = urllib.urlopen(url)
        data = u.read()
        return data


    def grab_by_post(self, url, params):
        """grab given url as local html by POST method"""
        encoded_params = urllib.urlencode(params)
        u = urllib.urlopen(url, encoded_params)
        data = u.read()
        return data


    def extractor(self, text):
        """extract wiki-page's text source from given text"""
        return self.get_content_by_id("wiki__text", text)


    def get_content_by_id(self, key_id, html):
        """get content from HTML by id"""
        # bsp = BeautifulSoup(text, fromEncoding="utf_8")
        bsp = BeautifulSoup(html)
        res = bsp.findAll('textarea', id=key_id)
        return "".join([item.string for item in res]).strip()


    def extract_anchors(self, html, url):
        """get content from HTML by id"""
        # bsp = BeautifulSoup(text, fromEncoding="utf_8")
        bsp = BeautifulSoup(html)
        res = bsp.findAll('a', dict(href=True))
        rex_abs = re.compile(r"^/")
        rex_rel = re.compile(r"^(?!http://|https://)")
        rex_protocol = re.compile(r"^[a-z]+:")
        rex_protocol_allow = re.compile(r"^(http://|https://)")

        if re.search(r"^http://[^/]+$", url):
            url = url + "/"
        try:
            hostname = re.search(r"^(http://[^/]+)/", url).group(1)
        except AttributeError:
            raise WikiGrabberError("no_hostname_in_url", url)
        try:
            url_basedir = re.search(r"^(.*/).*$", url).group(1)
        except AttributeError:
            raise WikiGrabberError("no_basedir_in_url", url)

        anchors = []
        for item in res:
            link_url = item["href"]

            # regularize
            if rex_protocol.search(link_url):
                if not rex_protocol_allow.search(link_url):
                    continue
            if rex_abs.search(link_url):
                link_url = hostname + link_url
            elif rex_rel.search(link_url):
                link_url = url_basedir + link_url

            anchors.append(link_url)
        return anchors

    


