#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import fileinput

URLREGEX = r'''(?i)(?:http|ftp)s?://[]:/?#@!$&'()*+,;=A-z\d\-._~%[]*'''
URLSERVICE = '''http://shorturl.com/make_shorturl.php?longurl=%s'''
SHORTREGEX = r'''(?s)id="txtfld".*?value\s*=\s*"(.*?)"'''
PREVIEWREGEX = r'''(?s)id="txtfld2".*?value\s*=\s*"(.*?)"'''
COUNTERREGEX = r'''(?s)id="txtfld3".*?value\s*=\s*"(.*?)"'''

def shrink(longurl):
    queryurl = URLSERVICE % urllib.quote(longurl)
    html = "\n".join(urllib2.urlopen(queryurl).readlines())
    shorturl = re.search(SHORTREGEX, html).group(1)
    return shorturl

def main():

    for line in fileinput.input():
        for match in re.finditer(URLREGEX, line):
            line = line.replace(match.group(), shrink(match.group()))
        print(" > %s" % line),


if __name__ == "__main__":
    exit(main())
