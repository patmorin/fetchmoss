#!/usr/bin/python3

import sys
import urllib
import urllib.request
import re
import time


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s <mossurl>\n".format(sys.argv[0]))
        sys.exit(-1)
    baseurl = sys.argv[1]
    if not baseurl.endswith('/'):
        sys.stderr.write("Error: url must end with trailing /\n")
        sys.exit(-2)
    print(baseurl)
    (filename, headers) = urllib.request.urlretrieve(baseurl, 'index.html')

    basedata = open(filename).read()

    newbasedata = re.sub(re.escape(baseurl), '', basedata)
    fp = open(filename, "w")
    fp.write(newbasedata)
    fp.close()

    pattern = re.compile(re.escape(baseurl) + r'([^"]*)')
    for m in re.finditer(pattern, basedata):
        url = m.group(0)
        filename = urllib.request.url2pathname(m.group(1))
        print(" {}".format(filename))
        (filename, headers) = urllib.request.urlretrieve(url, filename)
        matchdata = open(filename).read()
        pattern2 = re.compile(r'SRC="([^"]+)"')
        for m2 in re.finditer(pattern2, matchdata):
            murl = baseurl + m2.group(1)
            mfilename = urllib.request.url2pathname(m2.group(1))
            print("  {}".format(mfilename))
            urllib.request.urlretrieve(murl, mfilename)
        time.sleep(1)
