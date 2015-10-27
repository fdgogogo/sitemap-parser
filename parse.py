# coding: utf-8
import time

from bs4 import BeautifulSoup
import argparse
import concurrent
import requests
from concurrent.futures import Executor, ThreadPoolExecutor
import uuid

longest = 0


def get_urls(sitemaps):
    for sitemap in sitemaps:
        print('Parsing: %s' % sitemap)
        xml = requests.get(sitemap).text
        soup = BeautifulSoup(xml, 'html5lib')
        nodes = soup.findAll('loc')
        for node in nodes:
            url = node.text
            yield url


def parse(url):
    uid = str(uuid.uuid4())[:6]

    if args.full_url:
        output_url = url[:]
    else:
        output_url = url.replace('http://', '')
        output_url = output_url.replace('https://', '')
        if len(output_url) > 40:
            output_url = output_url[:20] + '...' + output_url[-20:]

    s = time.time()
    r = requests.get(url)
    te = time.time() - s

    print('%s\tParsed %s' % (uid, output_url))
    print('%s\t%s\t%s\t%sms' % (uid, r.status_code, len(r.content), te))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse urls from sitemap, support multiple domain, '
                    'separate by space.',
        # usage='get_urls.py example.com example2.com example3.com'
    )
    parser.add_argument('sitemaps', metavar='sitemaps', type=str, nargs='*',
                        help='sitemap urls separated by space.')
    parser.add_argument('-w', '--workers', dest='workers', type=int,
                        default=20, help='Concurrent workers, default 20')
    parser.add_argument('-F', '--full', dest='full_url',
                        action='store_true',
                        help='Print full url',
                        default=False)

    args = parser.parse_args()
    args = parser.parse_args()

    urls = [url for url in get_urls(args.sitemaps)]

    print('Parsing start')
    start = time.time()
    print('Url count: %s' % len(urls))

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.workers) as executor:
        future_to_url = {executor.submit(parse, url): url for url in
                         urls}
        for future in concurrent.futures.as_completed(future_to_url):
            _url = future_to_url[future]

    count = len(urls)
    time_e = time.time() - start
    avg = time_e % len(urls)
    print('------------------------------------------')
    print('Done')
    print('Count: %(count)s, total time: %(time_e)s, '
          'average_time: %(avg)s' % {
            'count': count,
            'time_e': time_e,
            'avg': avg
          })
