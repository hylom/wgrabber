#!/usr/bin/env python26
# -*- coding: utf-8 -*-

import unittest
import os.path
import wikipush
import codecs
import sfjp
import sys
import getpass


footer = """{{{ html
<div style="border:1px solid; background:#EEEEEE;padding:4px;margin-top:2em;">
<a href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img src="http://sourceforge.jp/projects/ffdshow-tryout/wiki/home/attach/cc-by-nc-sa.png" alt="cc-by-nc-sa" title="cc-by-nc-sa.png" height="15" width="80"></a> このWikiページは、<a href="%s">ffdshow wiki</a>を日本語訳したものです。
</div>
}}}
"""


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        config = {}

        # http://sourceforge.jp/projects/ffdshow-tryout/wiki/hogehoge?action=edit
        config["prefix"] = "http://sourceforge.jp/projects/ffdshow-tryout/wiki/"
        config["dir"] = "./push_video"
        config["max_recur"] = 10
        self.pusher = wikipush.WikiPusher(config)

    def test_push_by_post(self):
        """test push_by_post func"""
        return

        url = "http://sourceforge.jp/projects/ffdshow-tryout/wiki/home?action=update"
        bodytext = u"""= テストしてみる =
てすとてすと
ほげほげ
foobar

"""
        params = dict(textarea_height="24", text=bodytext, commit=u"保存", comment="")
        html = self.pusher.push_by_post(url, params)
        print html

    def test_login(self):
        sfjp_opener = sfjp.FancyURLopenerWithCookie()
        try:
            sfjp_opener.load_cookie("./cookie")
        except IOError:
            sys.stderr.write("cannot use cookie file. create.\n")

        if sfjp_opener.get_cookie() == "":
            try:
                uname = raw_input("user: ")
            except KeyboardInterrupt:
                sys.exit("\nabort.")

            try:
                passwd = getpass.getpass("login password:")
            except KeyboardInterrupt:
                sys.exit("\nabort.")
                if sfjp_opener.login(uname, passwd) != 1:
                    sys.exit("login error!")
                    
            sfjp_opener.login(uname, passwd)
            sfjp_opener.save_cookie("./cookie")


    def test_run(self):
        """test run func"""
        self.pusher.run()



# do unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
