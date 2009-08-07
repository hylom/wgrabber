#!/usr/bin/env python26
# -*- coding: utf-8 -*-

import unittest
import gtranslate
import codecs
import sys

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.english = """=  Welcome to the ffdshow wiki! 

The ffdshow wiki contains the '''online help''' of ffdshow and other project-related documentation. For more general information visit the [http://ffdshow-tryout.sourceforge.net/ home page] or just go straight to the [http://ffdshow-tryout.sourceforge.net/download.php download] page.[[BR]]
By the way, this wiki can be edited by '''everyone'''. Registering for an [http://ffdshow-tryout.sourceforge.net/wiki/home?do=register account] isn't necessary but recommended.

Have fun,[[BR]]
'''Your ffdshow team'''


==  Online help 
  * [FAQ FAQ]
  * [video_decoder_configuration Video decoder configuration]
  * [audio_decoder_configuration Audio decoder configuration]

==  About ffdshow 
  * [Changelog]   
  * [credits Credits]

==  Development 
  * [devel-building Building ffdshow]
  * [devel-translating Translating ffdshow]
  * [devel-controlling Controlling ffdshow remotely]

"""

    def test_translate(self):
        """test translatet func"""
        japanese = gtranslate.translate(self.english)
        print japanese


# do unittest
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
