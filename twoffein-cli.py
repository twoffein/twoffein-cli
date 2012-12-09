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

import pwd
import os
import sys
import twoffein
import cmd
import string
import time

home = pwd.getpwuid(os.getuid())[5]
if not os.access("%s/.twoffeinclirc" % home, os.F_OK|os.R_OK):
	f = open("%s/.twoffeinclirc" % home, "w")
	f.write("# twoffein cli client configuration\n")
	f.write("API_KEY = \"ABCDEFGHIJK\"")
	f.write("USER = \"h4xx0r\"")
	f.write("DRINKS = [ \"wasser\", \"cola\", \"schwarztee\" ]")
	f.close()
execfile("%s/.twoffeinclirc" % home )
del home

class TwoffeinCLI(cmd.Cmd):
	""" Command line client for Twoffein.com """
	
	intro = "Twoffein Command Line"
	prompt = "twoffein: "
	doc_header = "Commands"
	
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.twfn = twoffein.Twoffein( (USER, API_KEY) )
		
	def do_drink(self, drink, drink_with=""):
		ret = self.twfn.drink( twoffein.Drink(drink), ( None if drink_with == "" else drink_with) )
		print ret["code"]+':',
		if ret["code"]=="luna":
			print "Yeah!"
		elif ret["code"] == "pinkiepie":
			print "Chill mal! Nicht so viel auf einmal trinken!"
			print "Du darfst in "+str(ret["sleep"])+" Minuten wieder trinken."
		elif ret["code"] == "rarity":
			print "Bitte aktualisiere deinen API–Key in der Konfiguration!"
		elif ret["code"] == "sweetiebelle":
			print "Doppelt hält nicht immer besser! Du hast das gleiche eben schonmal getrunken."
		elif ret["code"] == "rainbowdash":
			print "Ganz böse! Niemals die twoffein–Server mit anfragen überfluten!"
		else:
			print ret["error"]
		
	def help_drink(self):
		print '\n'.join(['drink [drink id] [optional: user you drink with]', 'Drink something'])
		
	def do_get(self, action, profile_id=""):
		if action=="drinks":
			drinks = self.twfn.get_drinks()
			print "| Getränk                   | ID                  |"
			print "+---------------------------+---------------------+"
			for d in drinks:
				print "| ", string.ljust(d["drink"], 24), "|", string.ljust(d["key"], 19), "|"
			print "+---------------------------+---------------------+"

		elif action.startswith("profile"):
			profile = self.twfn.get_profile(profile_id)
			print "Profil von",profile["screen_name"]
			print ""
			print "Mitglied seit:", time.strftime("%d.%m %Y %H:%M:%S", time.localtime(int(profile["first_login"])))
			print "Getrunken:", profile["drunken"]
			print "Rang:", profile["rank"], "("+profile["rank_title"]+")"
			print "Lieblingsgetränk:",profile["drink"]
			print "Aktuelle Quest:",profile["quest"]
		
	def help_get(self):
		print '\n'.join(['get [profile|drinks] [profile_user]', '\tReturn the profile of a user or the list of drinks'])

	def do_cookie(self, target):
		ret = self.twfn.give_cookie(target)
		print ret["code"]+":",
		if ret.has_key("info"):
			print ret["info"]
		else:
			print ret["error"]
		
	def do_EOF(self, line):
		return True

def main():
	TwoffeinCLI().cmdloop()

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
