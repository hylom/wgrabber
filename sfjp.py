#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""wikigrab.py - Wiki Grabber"""

import urllib
import os
import os.path
import re
import copy
import httplib

BROWSER = "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7 (.NET CLR 3.5.30729) "
LOGIN_URL = "https://sourceforge.jp/account/login.php"
LOGIN_HOST = "sourceforge.jp"
LOGIN_PATH = "/account/login.php"

LOGIN_PARAM = {
    "return_to":"/my",
    "login":"1",
    "form_loginname":"",
    "form_pw":"",
    "stay_in_ssl":"1",
    "submit":"ログイン"
    }

class FancyURLopenerWithCookie(urllib.FancyURLopener):
    """URLopener for sf.jp"""
    def __init__(self, cookie="", *args, **kwargs):
        self.version = BROWSER
        urllib.FancyURLopener.__init__(self, *args, **kwargs)
        
        self.set_cookie(cookie)

    def regist_cookie(self):
        if self._cookie:
            self.addheaders.append(("Cookie", self._cookie))

    def set_cookie(self, cookie=""):
        self._cookie = cookie

    def get_cookie(self):
        return self._cookie

    def load_cookie(self, path):
        file_obj = open(path, "r")
        str_cookie = file_obj.readline()
        self.set_cookie(str_cookie)
        file_obj.close()

    def save_cookie(self, path):
        file_obj = open(path, "w")
        file_obj.write(self.get_cookie())
        file_obj.close()

    def login(self, user="", passwd=""):
        login_param = copy.deepcopy(LOGIN_PARAM)

        login_param["form_loginname"] = user
        login_param["form_pw"] = passwd

        encoded_data = urllib.urlencode(login_param)

        headers = {
            "User-Agent": BROWSER,
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
            }


        obj = httplib.HTTPSConnection(LOGIN_HOST)
        obj.request("POST", LOGIN_PATH, encoded_data, headers)
        resp = obj.getresponse()
        headers = resp.getheaders()

        for header in headers:
            if header[0] == "set-cookie":
                str_cookie = header[1]
                break
        else:
            return -1

        self.set_cookie(str_cookie)
        return 1
        

