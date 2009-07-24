#!/usr/bin/env python

import unittest
import os.path
import wikigrab

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        config = {}
        
        config["start_url"] = "http://ffdshow-tryout.sourceforge.net/wiki/home"
        config["prefix"] = "http://ffdshow-tryout.sourceforge.net/wiki/"
        config["output_dir"] = "./ffdshow"
        self.grabber = wikigrab.WikiGrabber(config)
        self.test_html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
 lang="en" dir="ltr">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>
    home    [ffdshow wiki]
  </title>
  </head>
<body class='sidebar_inside_left'>
<form action="" method="post" >
<input type="hidden" name="sectok" value="d1edf02df0138c3a7307e24a371115e9" />
<input type="hidden" name="id" value="home" />
<input type="hidden" name="rev" value="" />
<input type="hidden" name="date" value="1239099312" />
<input type="hidden" name="prefix" value="" />
<input type="hidden" name="suffix" value="" />
<input type="hidden" name="changecheck" value="288b43989cd8dfa23319573916dfd16d" />
<textarea name="wikitext" id="wiki__text" class="edit" cols="80" rows="10" tabindex="1" >
This is text codes.
foo bar hoge hoge
</textarea>
</form>
<div class="footerinc">
  <a  href="/wiki/feed.php" title="Recent changes RSS feed"><img src="/wiki/lib/tpl/sidebar/images/button-rss.png" width="80" height="15" alt="Recent changes RSS feed" /></a>
        <a  href="http://creativecommons.org/licenses/by-nc-sa/3.0/" rel="license" title="CC Attribution-Noncommercial-Share Alike 3.0 Unported"><img src="/wiki/lib/images/license/button/cc-by-nc-sa.png" width="80" height="15" alt="" /></a>
  <a  href="http://www.dokuwiki.org/donate" title="Donate"><img src="/wiki/lib/tpl/sidebar/images/button-donate.gif" alt="Donate" width="80" height="15" /></a>
  <a  href="http://www.php.net" title="Powered by PHP"><img src="/wiki/lib/tpl/sidebar/images/button-php.gif" width="80" height="15" alt="Powered by PHP" /></a>
  <a  href="http://validator.w3.org/check/referer" title="Valid XHTML 1.0"><img src="/wiki/lib/tpl/sidebar/images/button-xhtml.png" width="80" height="15" alt="Valid XHTML 1.0" /></a>
  <a  href="http://jigsaw.w3.org/css-validator/check/referer?profile=css3" title="Valid CSS"><img src="/wiki/lib/tpl/sidebar/images/button-css.png" width="80" height="15" alt="Valid CSS" /></a>
  <a  href="http://dokuwiki.org/" title="Driven by DokuWiki"><img src="/wiki/lib/tpl/sidebar/images/button-dw.png" width="80" height="15" alt="Driven by DokuWiki" /></a>
  <a  href="hogehoge" title="hogehoge"><img src="/wiki/lib/tpl/sidebar/images/button-dw.png" width="80" height="15" alt="Driven by DokuWiki" /></a>
</div>
</body>
</html>
"""


    def test_get_content_by_id(self):
        """test for get_content_by_id function"""

        ret_ok = """This is text codes.
foo bar hoge hoge"""

        ret = self.grabber.get_content_by_id("wiki__text", self.test_html)
        #print ret
        self.assertEqual(ret, ret_ok)


    def test_extract_anchors(self):
        """test for extract_anchors function"""

        ret_ok = ["http://ffdshow-tryout.sourceforge.net/wiki/feed.php",
                  "http://creativecommons.org/licenses/by-nc-sa/3.0/",
                  "http://www.dokuwiki.org/donate",
                  "http://www.php.net",
                  "http://validator.w3.org/check/referer",
                  "http://jigsaw.w3.org/css-validator/check/referer?profile=css3",
                  "http://dokuwiki.org/",
                  "http://ffdshow-tryout.sourceforge.net/wiki/hogehoge"]
        
        ret = self.grabber.extract_anchors(self.test_html, "http://ffdshow-tryout.sourceforge.net/wiki/home")
        self.assertEqual(len(ret), len(ret_ok))
        ret.sort()
        ret_ok.sort()
        for index in range(len(ret)):
            self.assertEqual(ret[index], ret_ok[index])


    def test_create_subdir(self):
        """test for _create_subdir function"""
        path = "./ffdshow/foo/bar/hoge.txt"
        self.grabber._create_dir_from_output_pathname(path)
        self.assertTrue(os.path.isdir("./ffdshow/foo/bar"))
        os.removedirs("./ffdshow/foo/bar")
        

    def test_run(self):
        """test for run function"""
        config = {}
        
        config["start_url"] = "http://ffdshow-tryout.sourceforge.net/wiki/home"
        config["prefix"] = "http://ffdshow-tryout.sourceforge.net/wiki/"
        config["output_dir"] = "./run_test"
        config["max_recur"] = "10"
        config["allow_rule"] = [r"^http://ffdshow-tryout.sourceforge.net/wiki/",]
        config["deny_rule"] = [r"\.[A-Za-z0-9]+$",]
        config["filename_subst_rule"] = [
            (":", "-"),
            ]
        config["rewrite_rule"] = [
            (r"^(.*)\?.*$", r"\1"),
            (r"^(.*)\#.*$", r"\1"),
            ]


        grabber = wikigrab.WikiGrabber(config)
        grabber.run()
        

# do unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
