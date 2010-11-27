#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os
import fileinput
from decoradores import Retry

URLREGEX = r'''(?i)(?:http|ftp)s?://[]:/?#@!$&'()*+,;=A-z\d\-._~%[]*'''
URLSERVICE = '''http://shorturl.com/make_shorturl.php'''
SHORTREGEX = r'''(?s)id="txtfld".*?value\s*=\s*"(.*?)"'''
COUNTERREGEX = r'''(?s)id="txtfld3".*?value\s*=\s*"(.*?)"'''
LOGFILE = os.path.expanduser('''~/.shorturl''')


@Retry(10)
def shrink(longurl, log=True):
    if len(longurl) < 30:
        return longurl
    else:
        longurl = urllib.quote_plus(longurl)
        data = urllib.urlencode({"longurl": longurl, "x": "30", "y": "7"})
        html = "\n".join(urllib2.urlopen(URLSERVICE, data).readlines())
        try:
            shorturl = re.search(SHORTREGEX, html).group(1)
        except:
            return None

        if log:
            counterurl = re.search(COUNTERREGEX, html).group(1)
            try:
                file = open(LOGFILE, "a")
            except:
                file = open(LOGFILE, "w")
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
