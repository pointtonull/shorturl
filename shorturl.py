#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import urllib
import re
import fileinput

URLREGEX = r'''(?:http|ftp)s?://[]:/?#@!$&'()*+,;=A-z\d\-._~%[]*'''

def main():

    for line in fileinput.input():
        for match in re.finditer(URLREGEX, line, re.IGNORECASE):
            print match.group()
            line = line.replace(match.group(), "busted xD")
        print(" > %s" % line),

if __name__ == "__main__":
    exit(main())
