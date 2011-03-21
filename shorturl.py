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
FIELDSEPARATOR = r'''*FS*'''


class Log(object):
    def __init__(self, logfile):
        self.logfile = logfile
        self.entries = dict((line.strip().split(FIELDSEPARATOR)
            for line in open(self.logfile).readlines()))

    def append(self, longurl, shorturl):
        with open(self.logfile, "a") as file:
            file.write(FIELDSEPARATOR.join((longurl, shorturl + "\n")))
        self.entries[shorturl] = longurl
        return True


@Retry(10)
def shrink(longurl, log=True):
    if len(longurl) < 30:
        return longurl
    elif longurl in global_log.entries:
        return global_log.entries[longurl]
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
            global_log.append(longurl, counterurl)

        return shorturl


def main():

    for line in fileinput.input():
        for match in re.finditer(URLREGEX, line):
            line = line.replace(match.group(), shrink(match.group()))
        print line,


if __name__ == "__main__":
    global_log = Log(LOGFILE)
    exit(main())
