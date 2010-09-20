#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os
import fileinput

URLREGEX = r'''(?i)(?:http|ftp)s?://[]:/?#@!$&'()*+,;=A-z\d\-._~%[]*'''
URLSERVICE = '''http://shorturl.com/make_shorturl.php'''
SHORTREGEX = r'''(?s)id="txtfld".*?value\s*=\s*"(.*?)"'''
COUNTERREGEX = r'''(?s)id="txtfld3".*?value\s*=\s*"(.*?)"'''
LOGFILE = os.path.expanduser('''~/.shorturl''')


def shrink(longurl, log=True):
    longurl = urllib.quote_plus(longurl)
    data = urllib.urlencode({"longurl": longurl, "x": "30", "y": "7"})
    html = "\n".join(urllib2.urlopen(URLSERVICE, data).readlines())
    shorturl = re.search(SHORTREGEX, html).group(1)

    if log:
        counterurl = re.search(COUNTERREGEX, html).group(1)
        file = open(LOGFILE, "a")
        file.write("%s %s\n" % (longurl, counterurl))
        file.close()


    return shorturl


def main():

    for line in fileinput.input():
        for match in re.finditer(URLREGEX, line):
            line = line.replace(match.group(), shrink(match.group()))
        print line,


if __name__ == "__main__":
    exit(main())
