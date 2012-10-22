#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Malte Bublitz, https://malte-bublitz.de
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR
# AND/OR CONTRIBUTORS OF WindowsInfo BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

import urllib2
import json
import StringIO
import pwd
import os
import sys

home = pwd.getpwuid(os.getuid())[5]
if not os.access("%s/.twoffeinclirc" % home, os.F_OK|os.R_OK):
	f = open("%s/.twoffeinclirc" % home, "w")
	f.write("# twoffein cli client configuration\n")
	f.write("API_KEY = \"ABCDEFGHIJK\"")
	f.write("USER = \"h4xx0r\"")
	f.close()
execfile("%s/.twoffeinclirc" % home )
del home


def main():
	if len(sys.argv)==2:
		drink_with = sys.argv[1]
	else:
		drink_with = ""
	print "[H[2J"
	print "Twoffein CLI–App"
	print ""
	if drink_with == "":
		print "Was willst du trinken?"
	else:
		print "Was willst du mit "+drink_with+" trinken?"
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
	if drink_with == "":
		response = urllib2.urlopen("http://twoffein.com/api/post/tweet/?screen_name="+USER+"&api_key="+API_KEY+"&drink="+drink)
	else:
		response = urllib2.urlopen("http://twoffein.com/api/post/tweet/?screen_name="+USER+"&api_key="+API_KEY+"&drink="+drink+"&target_screen_name="+drink_with)
	ret = json.load(StringIO.StringIO(response.read()))
	if ret["code"]=="luna":
		print "Yeah!"
	elif ret["code"] == "pinkiepie":
		print "Chill mal! Nicht so viel auf einmal trinken!"
	elif ret["code"] == "rarity":
		print "Bitte aktualisiere deinen API–Key in der Konfiguration!"
	elif ret["code"] == "sweetiebelle":
		print "Doppelt hält nicht immer besser! Du hast das gleiche eben schonmal getrunken."
	elif ret["code"] == "rainbowdash":
		print "Ganz böse! Niemals die twoffein–Server mit anfragen überfluten!"
	else:
		print "Da ist was schief gelaufen…"
		print ret["code"]+":",ret["error"]

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
