#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os.path
import wikipush
import codecs

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        config = {}

        # http://sourceforge.jp/projects/ffdshow-tryout/wiki/hogehoge?action=edit
        config["prefix"] = "http://sourceforge.jp/projects/ffdshow-tryout/wiki/"
        config["dir"] = "./push_test"
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

    def test_run(self):
        """test run func"""
        self.pusher.run()



# do unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
