# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

#Use numpy's DataSource, handles compressed files

ds = np.lib.DataSource()
fp = ds.open('http://datasets.connectmv.com/file/ammonia.csv')
from StringIO import StringIO
arr = np.genfromtxt(StringIO(fp.read()), names=True)

#Or you could use urllib

import urllib
fp2 = urllib.urlopen('http://datasets.connectmv.com/file/ammonia.csv')
arr2 = np.genfromtxt(StringIO(fp2.read()), names=True)

# Or use this canned routine

def loadurl(url, *args, **kwargs):
   from urllib import urlopen
   from cStringIO import StringIO
   fp = urlopen(url)
   return np.genfromtxt(StringIO(fp.read()), *args, **kwargs)

arr3 = loadurl('http://datasets.connectmv.com/file/ammonia.csv')