# coding: utf-8
import time

from bs4 import BeautifulSoup

import requests

def parse():
    url_count = 0
    start = time.time()
    longest = 0
    longest_url = ''
    for sitemap in sitemaps:
        xml = requests.get(sitemap).text
        soup = BeautifulSoup(xml, 'html5lib')
        nodes = soup.findAll('loc')
        for node in nodes:
            url = node.text
            url_count+=1
            print url
            s = time.time()
            r = requests.get(url)
	    te = (time.time() - s) * 1000
	    if te > longest:
	        longest = te
		longest_url = url
            print '%s\t%s\t%s' % (r.status_code, len(r.content), te)

    time_passed = time.time() - start
    print 'count: %s\t time: %s\t average: %s' % (url_count, time_passed, time_passed / float(url_count) * 1000)
    print 'slowest: %s %s' % ( longest, longest_url)

if __name__ == '__main__':
	parse()

