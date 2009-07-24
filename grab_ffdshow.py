#!/usr/bin/env python

import wikigrab


config = {}

config["start_url"] = "http://ffdshow-tryout.sourceforge.net/wiki/home"
config["prefix"] = "http://ffdshow-tryout.sourceforge.net/wiki/"
config["output_dir"] = "./ffdshow"
config["max_recur"] = 5

grabber = wikigrab.WikiGrabber(config)
grabber.run()

