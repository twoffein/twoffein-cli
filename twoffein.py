#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Malte Bublitz, https://malte-bublitz.de
# All rights reserved.
#
# Licensed under the 2 clause BSD license
#

API_KEY="ABCDEFGHIJK"

import urllib2
import json
import StringIO

def main():
	print "[H[2J"
	print "Twoffein CLI–App"
	print ""
	print "Was willst du trinken?"
	print ""
	print " => schwarztee"
	print " => mineralwasser"
	print " => wasser"
	print " => milch"
	print " => africola"
	print " => fritzcola"
	print " => cola"
	print " => colamix"
	print " => energiedrink"
	print " => kakao"
	print ""
	drink = str(raw_input()).strip()
	response = urllib2.urlopen("http://twoffein.com/api/post/tweet/?screen_name=malte70&api_key="+API_KEY+"&drink="+drink)
	ret = json.load(StringIO.StringIO(response.read()))
	if ret["code"]!="luna":
		print "Da ist was schief gelaufen…"
		print ret["code"]+":",ret["error"]
	else:
		print "Yeah!"

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
