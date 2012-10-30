__author__ = 'stone'
import urllib
url='http://a.bkeep.com/page/api/saInterface/searchServerInfo.htm?serviceTag=729HH2X'
page=urllib.urlopen(url)
data=page.read()
print data
