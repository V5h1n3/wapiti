#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Wapiti project (http://wapiti.sourceforge.net)
# Copyright (C) 2006-2013 Nicolas Surribas
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
import sys
import urllib
import jsoncookie
import requests
import getopt
import urlparse

if "_" not in dir():
    def _(s):
        return s

if len(sys.argv) < 3:
    sys.stderr.write("Usage python cookie.py [-p proxy_url] <cookie_file> <url> <arg1=val1> ...\n")
    sys.exit(1)

args = sys.argv[1:]
proxies = {}

try:
    opts, args = getopt.getopt(args, "p:", ["proxy="])
except getopt.GetoptError, e:
    print(e)
    sys.exit(2)
for o, a in opts:
    if o in ("-p", "--proxy"):
        parsed = urlparse.urlparse(a)
        proxies[parsed.scheme] = a

cookiefile = args[0]
url = args[1]
liste = []

if len(args) > 2:
    data = args[2:]
    for l in data:
        if "=" in l:
            liste.append(tuple(l.split("=")))
        else:
            sys.stderr.write("Usage python cookie.py [-p proxy_url] <cookie_file> <url> <arg1=val1> ...\n")
            print("Invalid key=value for web form: {0}".format(l))
            sys.exit(1)

params = urllib.urlencode(liste)

txheaders = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

session = requests.Session()
session.proxies = proxies

try:
    if params:
        txheaders['content-type'] = 'application/x-www-form-urlencoded'
        r = session.post(url, data=params, headers=txheaders)
    else:
        r = session.get(url, headers=txheaders)
except IOError, e:
        print(_("Error getting url {0}").format(url))
        print(e)
        sys.exit(1)

jc = jsoncookie.jsoncookie()
jc.open(cookiefile)
jc.addcookies(r.cookies)
jc.dump()
jc.close()
